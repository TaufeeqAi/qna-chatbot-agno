from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status, Query
from typing import Optional, Literal
from app.core.config import get_settings
from app.utils.pdf_utils import ingest_pdf
from app.utils.arxiv_utils import fetch_arxiv_paper
from app.utils.web_utils import fetch_webpage_content, convert_text_to_pdf_bytes
from app.core.secuirty import verify_access_token

router = APIRouter()
settings = get_settings()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def ingest_document(
    token_data: dict = Depends(verify_access_token),
    source_type: Literal["file", "arxiv", "url"] = Query("file", description="Type of the source to ingest."),
    source_identifier: Optional[str] = Query(None, description="arXiv ID or URL, required if source_type is 'arxiv' or 'url'."),
    file: Optional[UploadFile] = File(None, description="PDF file to upload, required if source_type is 'file'.")
):
    user_id = int(token_data.get("sub"))
    pdf_bytes_content: Optional[bytes] = None
    document_name = "document" # Default name, will be updated

    if source_type == "file":
        if not file:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is required for source_type 'file'.")
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are supported for 'file' source_type.")
        pdf_bytes_content = await file.read()
        document_name = file.filename
    
    elif source_type == "arxiv":
        if not source_identifier:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="source_identifier (arXiv ID) is required for source_type 'arxiv'.")
        try:
            pdf_bytes_content = fetch_arxiv_paper(source_identifier)
            if not pdf_bytes_content:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not fetch paper from arXiv with ID: {source_identifier}")
            document_name = f"{source_identifier}.pdf"
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching arXiv paper: {str(e)}")

    elif source_type == "url":
        if not source_identifier:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="source_identifier (URL) is required for source_type 'url'.")
        try:
            text_content = fetch_webpage_content(source_identifier)
            if not text_content:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not fetch or process content from URL: {source_identifier}")
            
            pdf_bytes_content = convert_text_to_pdf_bytes(text_content, title=source_identifier)
            if not pdf_bytes_content:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Could not convert webpage content to PDF for URL: {source_identifier}")
            document_name = f"webpage_{source_identifier.split('//')[-1].split('/')[0]}.pdf" # Generate a name
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error processing URL: {str(e)}")
            
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid source_type. Must be 'file', 'arxiv', or 'url'.")

    if not pdf_bytes_content:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to obtain PDF content.")

    try:
        # Assuming ingest_pdf can take document_name or you adjust it
        ingest_pdf(
            file_bytes=pdf_bytes_content,
            user_id=user_id,
            vector_db_url=settings.VECTOR_DB_URL,
            vector_api_key=settings.SECRET_KEY, # Ensure this is correct
            document_name=document_name # Pass the document name
        )
    except Exception as e:
        # Log the exception e for more details on the server
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to ingest document: {str(e)}")

    return {"detail": f"Document '{document_name}' from '{source_type}' ingested and indexed successfully."}
