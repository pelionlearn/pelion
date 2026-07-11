from pathlib import Path
import shutil

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from api.routers import users, documents, classes, class_members


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

# UPLOAD_DIR = Path("uploads")
# UPLOAD_DIR.mkdir(exist_ok=True)

app.include_router(users.router)
app.include_router(classes.router)
app.include_router(documents.router)
app.include_router(class_members.router)


@app.get("/")
async def root():
    return {"status": "API is running"}
