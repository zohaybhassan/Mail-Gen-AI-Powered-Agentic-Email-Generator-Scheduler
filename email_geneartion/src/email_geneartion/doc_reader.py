import os

def read_document(doc_path: str) -> str:
    """
    Reads content from a .txt, .pdf, or .docx file and returns it as plain text.
    Returns error message string if failed.
    """
    ext = os.path.splitext(doc_path)[1].lower()

    if ext == '.txt':
        return _read_txt(doc_path)
    elif ext == '.pdf':
        return _read_pdf(doc_path)
    elif ext == '.docx':
        return _read_docx(doc_path)
    else:
        return f"ERROR: Unsupported file format '{ext}'. Supported: .txt, .pdf, .docx"

# --- Handlers for each type ---

def _read_txt(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"ERROR reading .txt file: {str(e)}"

def _read_pdf(path: str) -> str:
    try:
        import PyPDF2
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return '\n'.join([page.extract_text() for page in reader.pages if page.extract_text()])
    except ImportError:
        return "ERROR: PyPDF2 not installed. Run: pip install PyPDF2"
    except Exception as e:
        return f"ERROR reading .pdf file: {str(e)}"

def _read_docx(path: str) -> str:
    try:
        import docx
        doc = docx.Document(path)
        return '\n'.join([para.text for para in doc.paragraphs])
    except ImportError:
        return "ERROR: python-docx not installed. Run: pip install python-docx"
    except Exception as e:
        return f"ERROR reading .docx file: {str(e)}"

