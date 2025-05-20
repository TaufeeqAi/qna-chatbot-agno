import requests
from bs4 import BeautifulSoup
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from typing import Optional

def fetch_webpage_content(url: str) -> Optional[str]:
    """
    Fetches and extracts textual content from a web page.

    Args:
        url: The URL of the web page.

    Returns:
        The extracted textual content as a string, or None if an error occurs.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Check content type
        if 'text/html' not in response.headers.get('Content-Type', ''):
            print(f"URL {url} does not point to HTML content.")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # Get text
        # Try to find main content areas, otherwise fall back to body
        main_content = soup.find('main') or soup.find('article') or soup.body
        if main_content:
            text = main_content.get_text(separator='\n', strip=True)
        else:
            text = soup.get_text(separator='\n', strip=True)
        
        # Basic cleaning: remove excessive newlines
        cleaned_text = "\n".join(line for line in text.splitlines() if line.strip())
        
        return cleaned_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while fetching webpage content from {url}: {e}")
        return None

def convert_text_to_pdf_bytes(text_content: str, title: str = "Webpage Content") -> Optional[bytes]:
    """
    Converts a string of text content into PDF bytes using ReportLab.

    Args:
        text_content: The string content to convert.
        title: An optional title for the PDF document.

    Returns:
        The PDF content as bytes if successful, None otherwise.
    """
    if not text_content:
        print("No text content provided to convert to PDF.")
        return None

    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, title=title)
        styles = getSampleStyleSheet()
        
        # Split text into paragraphs to handle long text and preserve line breaks somewhat
        story = []
        for paragraph_text in text_content.split('\n'):
            if paragraph_text.strip(): # Add non-empty paragraphs
                p = Paragraph(paragraph_text, styles['Normal'])
                story.append(p)
            # else: # Could add a Spacer for blank lines if desired
            #     story.append(Spacer(1, 0.2*inch))

        if not story: # Handle case where text_content might be all whitespace
            print("Text content resulted in no printable paragraphs.")
            return None
            
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

    except Exception as e:
        print(f"Error converting text to PDF: {e}")
        return None

if __name__ == '__main__':
    # Example Usage for fetch_webpage_content
    test_url_html = "https://www.google.com" # A simple page
    test_url_non_html = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png" # Non-HTML
    test_url_error = "https://thisshouldnotexist.xyz"

    print(f"\n--- Testing fetch_webpage_content ---")
    content_html = fetch_webpage_content(test_url_html)
    if content_html:
        print(f"Successfully fetched content from {test_url_html}. First 100 chars: {content_html[:100]}...")
    else:
        print(f"Failed to fetch content from {test_url_html}.")

    content_non_html = fetch_webpage_content(test_url_non_html)
    if not content_non_html:
        print(f"Correctly handled non-HTML URL: {test_url_non_html}")

    content_error = fetch_webpage_content(test_url_error)
    if not content_error:
        print(f"Correctly handled error URL: {test_url_error}")

    # Example Usage for convert_text_to_pdf_bytes
    print(f"\n--- Testing convert_text_to_pdf_bytes ---")
    sample_text = "This is a test document.\nIt has multiple lines.\n\nAnd even some empty ones."
    pdf_bytes = convert_text_to_pdf_bytes(sample_text, title="Test Document")
    if pdf_bytes:
        print(f"Successfully converted text to PDF. Size: {len(pdf_bytes)} bytes.")
        # You could save it to a file to test:
        # with open("webpage_text.pdf", "wb") as f:
        #     f.write(pdf_bytes)
        # print("Saved text_to_pdf.pdf")
    else:
        print("Failed to convert text to PDF.")

    empty_text_pdf = convert_text_to_pdf_bytes("")
    if not empty_text_pdf:
        print("Correctly handled empty string for PDF conversion.")
    
    whitespace_text_pdf = convert_text_to_pdf_bytes("   \n   \n ")
    if not whitespace_text_pdf:
        print("Correctly handled whitespace-only string for PDF conversion.")
