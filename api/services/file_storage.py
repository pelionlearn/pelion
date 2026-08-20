from fastapi import UploadFile
from uuid import UUID
import shutil
from pathlib import Path
import os

STORAGE_LOCATION = Path(os.environ["STORAGE_LOCATION"])


def save_file(file: UploadFile, documentId: UUID):
    destination = STORAGE_LOCATION / str(documentId)

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # TODO: add error handling for failure to write

    return {
        "success": True,
        "filename": file.filename,
        "content_type": file.content_type,
        "size": destination.stat().st_size,
    }
