import PyPDF2
import docx
import io

def extract_text(file_stream, mimetype):
    """Extracts text from a file stream based on its mimetype."""
    text = ""
    if mimetype == 'application/pdf':
        reader = PyPDF2.PdfReader(file_stream)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        doc = docx.Document(file_stream)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif mimetype == 'text/plain':
        text = file_stream.read().decode('utf-8')
    return text
