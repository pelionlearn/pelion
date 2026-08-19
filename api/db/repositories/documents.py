from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Document, Classroom
from uuid import UUID
from exceptions import errors


async def create_document(
    db: AsyncSession,
    file_name: str,
    file_url: str | None,
    content_type: str | None,
    size: int,
    classroom_id: UUID,
):
    classroom = await db.get(Classroom, classroom_id)
    if classroom is None:
        raise errors.NotFoundError(f"Classroom {classroom_id} not found")
    obj = Document(
        file_name=file_name,
        file_url=file_url,
        content_type=content_type,
        size=size,
        classroom_id=classroom_id,
    )
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_document(db: AsyncSession, document_id, classroom_id):
    stmt = select(Document).where(
        Document.id == document_id, Document.classroom_id == classroom_id
    )
    obj = (await db.scalars(stmt)).one_or_none()
    if obj is None:
        raise errors.NotFoundError(f"Document {document_id} not found")
    await db.delete(obj)
    await db.commit()
    return obj


async def get_document(db: AsyncSession, document_id, classroom_id):
    stmt = select(Document).where(
        Document.id == document_id, Document.classroom_id == classroom_id
    )
    obj = (await db.scalars(stmt)).one_or_none()
    if obj is None:
        raise errors.NotFoundError(f"Document {document_id} not found")

    return obj


async def rename_document(db: AsyncSession, document_id, classroom_id, name: str):
    stmt = select(Document).where(
        Document.id == document_id, Document.classroom_id == classroom_id
    )
    document = (await db.scalars(stmt)).one_or_none()

    if document is None:
        raise errors.NotFoundError(f"Document {document_id} not found")

    document.file_name = name

    await db.commit()
    await db.refresh(document)

    return document


async def get_class_documents(db: AsyncSession, classroom_id: UUID):
    stmt = select(Document).where(Document.classroom_id == classroom_id)
    documents = (await db.scalars(stmt)).all()
    return documents
