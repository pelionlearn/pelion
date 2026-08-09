from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from db.models import Document, Classroom
from uuid import UUID
from exceptions import errors


async def create_document(
    db: AsyncSession, file_name: str, file_url: str, classroom_id: UUID
):
    classroom = await db.get(Classroom, classroom_id)
    if classroom is None:
        raise errors.NotFoundError(f"Classroom {classroom_id} not found")
    obj = Document(file_name=file_name, file_url=file_url, classroom_id=classroom_id)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_document(db: AsyncSession, id):
    obj = await db.get(Document, id)
    if obj is None:
        raise errors.NotFoundError(f"Document {id} not found")
    await db.delete(obj)
    await db.commit()
    return obj


async def get_document(db: AsyncSession, document_id):
    obj = await db.get(Document, document_id)
    if obj is None:
        raise errors.NotFoundError(f"Document {document_id} not found")

    return obj


async def rename_document(db: AsyncSession, id, name: str):
    document = await db.get(Document, id)

    if document is None:
        raise errors.NotFoundError(f"Document {id} not found")

    document.file_name = name

    await db.commit()
    await db.refresh(document)

    return document


async def get_document_class(db: AsyncSession, id):
    document = await db.get(Document, id)
    if document is None:
        raise errors.NotFoundError(f"Document {id} not found")
    return document.classroom


async def get_class_documents(db: AsyncSession, classroom_id: UUID):
    stmt = (
        select(Classroom)
        .where(Classroom.id == classroom_id)
        .options(selectinload(Classroom.documents))
    )
    class_obj = (await db.scalars(stmt)).one_or_none()
    if class_obj is None:
        raise errors.NotFoundError(f"Classroom {classroom_id} not found")
    return class_obj.documents
