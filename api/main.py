from pathlib import Path
import shutil

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from routers import documents, classroom_members, classrooms, coref
from exceptions import errors, handlers

from auth.authentication import fastapi_users, auth_backend
from schemas.users import UserCreate, UserRead, UserUpdate
from auth.authentication import google_client, OAUTH_SECRET


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
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

# users route with fastapi users
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)

# general db routes
app.include_router(classrooms.router)
app.include_router(documents.router)
app.include_router(classroom_members.router)

# /auth/login + logout
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["Auth"]
)

# /auth/register
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_oauth_router(
        oauth_client=google_client,
        backend=auth_backend,
        state_secret=OAUTH_SECRET,
        associate_by_email=True,
    ),
    prefix="/auth/google",
    tags=["auth"],
)

# coreference resolution api
app.include_router(coref.router)


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
