from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from app.core.config import get_settings
from app.utils.pdf_utils import ingest_pdf
from app.core.secuirty import verify_access_token

router = APIRouter()

settings = get_settings()

@router.post("/", status_code=201)
async def upload_pdf(
    file: UploadFile,
    token_data: dict = Depends(verify_access_token)
):
    user_id = int(token_data.get("sub"))  # or however you map JWT sub → user ID
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported."
        )

    contents = await file.read()
    try:
        ingest_pdf(
            file_bytes=contents,
            user_id=user_id,
            vector_db_url=settings.VECTOR_DB_URL,
            vector_api_key=settings.SECRET_KEY  # or separate PINECONE_KEY in .env
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to ingest PDF: {e}"
        )
    return {"detail": "PDF ingested and indexed successfully."}
