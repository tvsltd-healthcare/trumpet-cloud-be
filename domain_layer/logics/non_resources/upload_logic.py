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

        print('=======file',file.filename)
        

    except Exception as e:
        print(f"Error: {e}")
        return {"message": str(e), "status_code": 500}