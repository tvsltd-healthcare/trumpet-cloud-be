import os
import time
import uuid
from pathlib import Path
from domain_layer.response_formatter import ResponseFormatter

# Configuration constants
OUTPUT_DIR = os.getenv('FILE_UPLOAD_ABS_DIR')

ALLOWED_DOCUMENT_TYPES = [
    # Images
    "image/jpeg",  # .jpg, .jpeg
    "image/png",   # .png

    # Documents
    "application/pdf",                                                         # .pdf
    "application/msword",                                                      # .doc (and sometimes .docx)
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document", # .docx

    # Spreadsheets
    "application/vnd.ms-excel",                                          # .xls (and sometimes .xlsx)
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", # .xlsx
    "application/vnd.oasis.opendocument.spreadsheet",

    # Presentations
    "application/vnd.ms-powerpoint",                                             # .ppt (and sometimes .pptx)
    "application/vnd.openxmlformats-officedocument.presentationml.presentation", # .pptx
]

def upload_file_to_disk(file) -> dict:
    """
    Save an uploaded file to the output directory with a unique filename.
    
    Args:
        file: The uploaded file object (e.g., FastAPI UploadFile).
        
    Returns:
        tuple: (unique_filename, Path to the saved file)
        
    Raises:
        ValueError: If the file is invalid or missing a filename.
        IOError: If file operations fail (e.g., disk full, permissions).
    """
    response_formatter = ResponseFormatter()

    if not file or not getattr(file, 'filename', None):
        raise ValueError('Invalid file content.')

    if file.content_type not in ALLOWED_DOCUMENT_TYPES:
        raise ValueError('Invalid file type.')

    # Create output directory
    file_dir = Path(OUTPUT_DIR).absolute()
    file_dir.mkdir(exist_ok=True)

    # Generate unique filename with timestamp and UUID
    unique_filename = f"file_{uuid.uuid4()}_{Path(file.filename).suffix}"
    file_path = file_dir / unique_filename

    try:
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        return {
            "file_name": file.filename,
            "file_path": (f"{OUTPUT_DIR}/{unique_filename}"),
            "file_size": file.size,
            "file_mime_type": file.headers.get('content-type')
        }

    except Exception as e:
        return response_formatter.error(str(e), 500)
