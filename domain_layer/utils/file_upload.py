import os
import time
from pathlib import Path

# Configuration constants
OUTPUT_DIR = os.getenv('FILE_UPLOAD_ABS_DIR')


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
    try:
        # Validate file input
        if not file or not getattr(file, 'filename', None):
            raise ValueError("Invalid or missing file")

        # Create output directory
        file_dir = Path(OUTPUT_DIR).absolute()
        file_dir.mkdir(exist_ok=True)

        # Generate unique filename with timestamp and UUID
        unique_filename = f"file_{time.time()}_{Path(file.filename).suffix or ".bin"}"
        file_path = file_dir / unique_filename

        # Read and write file contents
        contents = file.file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        return {
            "file_name": unique_filename,
            "file_path": (f"{OUTPUT_DIR}/{unique_filename}"),
            "file_size": file.size,
            "file_mime_type": file.headers.get('content-type')
        }

    except ValueError as e:
        raise ValueError(f"Invalid file input: {e}")
    except IOError as e:
        raise IOError(f"File operation failed: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error during file upload: {e}", exc_info=True)
