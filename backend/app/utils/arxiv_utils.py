import arxiv
from typing import Optional

def fetch_arxiv_paper(arxiv_id: str) -> Optional[bytes]:
    """
    Fetches a paper from arXiv based on its ID and returns the PDF content as bytes.

    Args:
        arxiv_id: The ID of the paper on arXiv (e.g., "1706.03762").

    Returns:
        The PDF content as bytes if successful, None otherwise.
    """
    try:
        # Search for the paper by ID
        search = arxiv.Search(id_list=[arxiv_id])
        paper = next(search.results())

        if paper and paper.pdf_url:
            # Download the PDF content
            pdf_content = paper.download_pdf()
            return pdf_content
        else:
            print(f"Could not find PDF URL for arXiv ID: {arxiv_id}")
            return None
    except StopIteration:
        print(f"Paper with arXiv ID '{arxiv_id}' not found.")
        return None
    except ConnectionError as e:
        print(f"Connection error while fetching arXiv ID '{arxiv_id}': {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while fetching arXiv ID '{arxiv_id}': {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # Make sure to have an internet connection for this to work.
    # Replace with a valid arXiv ID.
    example_arxiv_id = "1706.03762" # Transformer paper
    pdf_bytes = fetch_arxiv_paper(example_arxiv_id)

    if pdf_bytes:
        print(f"Successfully fetched PDF for {example_arxiv_id}. Size: {len(pdf_bytes)} bytes.")
        # You could save it to a file to test:
        # with open(f"{example_arxiv_id}.pdf", "wb") as f:
        #     f.write(pdf_bytes)
        # print(f"Saved PDF to {example_arxiv_id}.pdf")
    else:
        print(f"Failed to fetch PDF for {example_arxiv_id}.")

    example_invalid_arxiv_id = "xxxx.xxxx" # Invalid ID
    pdf_bytes_invalid = fetch_arxiv_paper(example_invalid_arxiv_id)
    if not pdf_bytes_invalid:
        print(f"Correctly handled invalid arXiv ID: {example_invalid_arxiv_id}")

    # Test with a non-existent ID
    example_non_existent_id = "9999.99999"
    pdf_bytes_non_existent = fetch_arxiv_paper(example_non_existent_id)
    if not pdf_bytes_non_existent:
        print(f"Correctly handled non-existent arXiv ID: {example_non_existent_id}")
