from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from uuid import UUID

from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from auth.authorization import require_classroom_member, require_document_in_class
from db import repositories
from db.database import get_db
from schemas.documents import DocumentResponse
from services.file_storage import STORAGE_LOCATION, save_file

router = APIRouter(prefix="/classrooms/{classroom_id}/documents", tags=["Documents"])


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    classroom_id: UUID,
    document_id: UUID,
    _: None = Depends(require_classroom_member),
    db: AsyncSession = Depends(get_db),
):
    return await repositories.documents.get_document(db, document_id, classroom_id)


@router.get("/{document_id}/file")
async def get_document_file(
    classroom_id: UUID,
    document_id: UUID,
    _memberOfClass: None = Depends(require_classroom_member),
    _documentInClass: None = Depends(require_document_in_class),
    db: AsyncSession = Depends(get_db),
):
    file_path = STORAGE_LOCATION / str(document_id)
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)


@router.get("/", response_model=list[DocumentResponse])
async def get_documents(
    classroom_id: UUID,
    _: None = Depends(require_classroom_member),
    db: AsyncSession = Depends(get_db),
):
    return await repositories.documents.get_class_documents(db, classroom_id)


@router.post("/", response_model=DocumentResponse)
async def create_document(
    classroom_id: UUID,
    file: UploadFile = File(...),
    # document: DocumentCreateRequest,
    _: None = Depends(require_classroom_member),
    db: AsyncSession = Depends(get_db),
):

    file_name = file.filename
    file_url = None
    content_type = file.content_type
    size = file.size

    # TODO: change the order here. it should be store file then add to db

    if file_name is None:
        raise HTTPException(status_code=400, detail="File name is required")
    if size is None:
        raise HTTPException(status_code=400, detail="Could not determine file size")

    doc = await repositories.documents.create_document(
        db, file_name, file_url, content_type, size, classroom_id
    )

    await save_file(file, classroom_id, doc.id)

    return doc


@router.delete("/{document_id}", response_model=DocumentResponse)
async def delete_document(
    classroom_id: UUID,
    document_id: UUID,
    _: None = Depends(require_classroom_member),
    db: AsyncSession = Depends(get_db),
):
    return await repositories.documents.delete_document(db, document_id, classroom_id)
