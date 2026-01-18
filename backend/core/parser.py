import PyPDF2
import docx
import io
from typing import Optional


def extract_text(file_stream, mimetype: str) -> Optional[str]:
    """
    Extracts text from a file stream based on its mimetype.
    
    Args:
        file_stream: File stream object
        mimetype: MIME type of the file
        
    Returns:
        Extracted text as string, or None if extraction fails
    """
    text = ""
    try:
        if mimetype == 'application/pdf':
            reader = PyPDF2.PdfReader(file_stream)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        elif mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            doc = docx.Document(file_stream)
            for para in doc.paragraphs:
                if para.text:
                    text += para.text + "\n"
        elif mimetype == 'text/plain':
            text = file_stream.read().decode('utf-8')
        else:
            return None
    except Exception as e:
        # Log error in production (using print for now)
        print(f"Error extracting text from {mimetype}: {e}")
        return None
    
    return text if text.strip() else None
