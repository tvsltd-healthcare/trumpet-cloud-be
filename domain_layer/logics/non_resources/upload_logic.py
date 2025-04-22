import os
import anyio
from datetime import datetime
import pandas as pd


def execute(request):
    if request is None:
        print("Request is None")
        return {"message": "Invalid request", "status_code": 400}
    
    try:
        print('===== Processing Request =====')
        body = anyio.from_thread.run(request.form)
        file = body.get("file")

        if file is None:
            return {"message": "No file provided", "status_code": 400}

        
        file_dir = os.path.abspath('output')

        # # Create a target directory
        os.makedirs(file_dir, exist_ok=True)
        # os.makedirs(file_paths, exist_ok=True)

        # # Use the original filename or generate a unique one to avoid conflicts
        original_filename = file.filename
        file_extension = os.path.splitext(original_filename)[1]  # Get file extension (e.g., .pdf, .png)
        unique_filename = f"file_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
        # file_paths = os.path.abspath('output/output_er.md')
        file_path = os.path.join(file_dir, unique_filename)
        print('file_path', file_path)

        # # Save the file
        # file_path = os.path.join(file_paths, unique_filename)

        contents = pd.read_excel(file_path)
        # contents = anyio.from_thread.run(file.read)
        print('contents', contents)

        # # Write the file content as-is (no pickle serialization)
        # with open(file_path, "wb") as f:
        #     f.write(contents)

        # # file_path = result["path"]  # Get path from the response
        # if os.path.exists(file_path):
        #     print(f"File exists at {file_path}")
        # else:
        #     print("File does not exist")

        # return {"message": file_path, "path": file_path, "status_code": 200}

    except Exception as e:
        print(f"Error: {e}")
        return {"message": str(e), "status_code": 500}