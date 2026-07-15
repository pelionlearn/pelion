from fastapi import APIRouter, Depends
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from db import repositories
from db.database import get_db
from schemas.documents import DocumentCreateRequest, DocumentResponse

router = APIRouter(prefix="/classrooms/{classroom_id}/documents", tags=["Documents"])


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    classroom_id: UUID, document_id: UUID, db: AsyncSession = Depends(get_db)
):
    return await repositories.documents.get_document(db, document_id)


@router.get("/", response_model=list[DocumentResponse])
async def get_documents(classroom_id: UUID, db: AsyncSession = Depends(get_db)):
    return await repositories.documents.get_class_documents(db, classroom_id)


@router.post("/", response_model=DocumentResponse)
async def create_document(
    classroom_id: UUID,
    document: DocumentCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    return await repositories.documents.create_document(
        db, document.file_name, document.file_url, classroom_id
    )


@router.delete("/{document_id}", response_model=DocumentResponse)
async def delete_document(
    classroom_id: UUID, document_id: UUID, db: AsyncSession = Depends(get_db)
):
    return await repositories.documents.delete_document(db, document_id)
