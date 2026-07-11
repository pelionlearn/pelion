from fastapi import APIRouter
from uuid import UUID
from db import repositories
from api.schemas.documents import DocumentCreate, DocumentResponse

router = APIRouter(prefix="/classes/{class_id}/documents", tags=["Documents"])


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(class_id: UUID, document_id: UUID):
    return repositories.documents.get_document(document_id)


@router.get("/", response_model=list[DocumentResponse])
async def get_documents(class_id: UUID):
    return repositories.documents.get_class_documents(class_id)


@router.post("/", response_model=DocumentResponse)
async def create_document(class_id: UUID, document: DocumentCreate):
    return repositories.documents.create_document(
        document.file_name, document.file_url, class_id
    )


@router.delete("/{document_id}", response_model=DocumentResponse)
async def delete_document(class_id: UUID, document_id: UUID):
    return repositories.documents.delete_document(document_id)
