from fastapi import APIRouter, Depends
from uuid import UUID

from sqlalchemy.orm import Session
from db import repositories
from db.database import get_db
from schemas.documents import DocumentCreateRequest, DocumentCreateResponse

router = APIRouter(prefix="/classrooms/{classroom_id}/documents", tags=["Documents"])


@router.get("/{document_id}", response_model=DocumentCreateResponse)
async def get_document(
    classroom_id: UUID, document_id: UUID, db: Session = Depends(get_db)
):
    return repositories.documents.get_document(db, document_id)


@router.get("/", response_model=list[DocumentCreateResponse])
async def get_documents(classroom_id: UUID, db: Session = Depends(get_db)):
    return repositories.documents.get_class_documents(db, classroom_id)


@router.post("/", response_model=DocumentCreateResponse)
async def create_document(
    classroom_id: UUID, document: DocumentCreateRequest, db: Session = Depends(get_db)
):
    return repositories.documents.create_document(
        db, document.file_name, document.file_url, classroom_id
    )


@router.delete("/{document_id}", response_model=DocumentCreateResponse)
async def delete_document(
    classroom_id: UUID, document_id: UUID, db: Session = Depends(get_db)
):
    return repositories.documents.delete_document(db, document_id)
