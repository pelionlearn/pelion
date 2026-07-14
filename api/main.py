from pathlib import Path
import shutil

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from routers import users, documents, classroom_members, classrooms
from exceptions import errors, handlers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


app.add_exception_handler(errors.NotFoundError, handlers.not_found_handler)
app.add_exception_handler(errors.ConflictError, handlers.conflict_handler)
app.add_exception_handler(errors.ValidationError, handlers.validation_handler)
app.add_exception_handler(errors.AuthenticationError, handlers.authentication_handler)
app.add_exception_handler(errors.AuthorizationError, handlers.authorization_handler)
app.add_exception_handler(errors.NotFoundError, handlers.not_found_handler)
app.add_exception_handler(
    errors.ExternalServiceError, handlers.external_service_handler
)

app.include_router(users.router)
app.include_router(classrooms.router)
app.include_router(documents.router)
app.include_router(classroom_members.router)


@app.get("/")
async def root():
    return {"status": "API is running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.filename is None:
        raise Exception

    destination = UPLOAD_DIR / file.filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "success": True,
        "filename": file.filename,
        "content_type": file.content_type,
        "size": destination.stat().st_size,
    }
