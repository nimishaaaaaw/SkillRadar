import pdfplumber
import io


def extract_text_from_pdf(file_storage):
    """
    Extract text from an uploaded PDF file.
    Accepts a Flask FileStorage object.
    Returns extracted text as a string.
    """
    text = ""
    try:
        # Read file bytes into memory — don't save to disk
        file_bytes = file_storage.read()
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        text = ""
        print(f"PDF extraction error: {e}")

    return text.strip()


def is_valid_pdf(file_storage):
    """
    Check if uploaded file is a valid non-empty PDF.
    Returns True/False.
    """
    try:
        file_bytes = file_storage.read()
        file_storage.seek(0)  # Reset pointer after reading
        if not file_bytes:
            return False
        # PDF files start with %PDF
        if not file_bytes[:4] == b'%PDF':
            return False
        return True
    except Exception:
        return False


def get_file_size_kb(file_storage):
    """
    Returns file size in KB.
    """
    try:
        file_storage.seek(0, 2)       # Seek to end
        size = file_storage.tell()    # Get position = size in bytes
        file_storage.seek(0)          # Reset pointer
        return round(size / 1024, 1)
    except Exception:
        return 0