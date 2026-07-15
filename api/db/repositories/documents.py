from sqlalchemy.orm import Session
from db.models import Document, Classroom
from uuid import UUID
from exceptions import errors


def create_document(db: Session, file_name: str, file_url: str, classroom_id: UUID):
    obj = Document(file_name=file_name, file_url=file_url, classroom_id=classroom_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_document(db: Session, id):
    obj = db.get(Document, id)
    if obj is None:
        raise errors.NotFoundError(f"Document {id} not found")
    db.delete(obj)
    db.commit()
    return obj


def get_document(db: Session, id):
    obj = db.get(Document, id)
    if obj is None:
        raise errors.NotFoundError(f"Document {id} not found")
    return obj


def rename_document(db: Session, id, name: str):
    document = db.get(Document, id)

    if document is None:
        raise errors.NotFoundError(f"Document {id} not found")

    document.file_name = name

    db.commit()
    db.refresh(document)

    return document


def get_document_class(db: Session, id):
    document = db.get(Document, id)
    if document is None:
        raise errors.NotFoundError(f"Document {id} not found")
    return document.classroom


def get_class_documents(db: Session, classroom_id: UUID):
    class_obj = db.get(Classroom, classroom_id)
    if class_obj is None:
        raise errors.NotFoundError(f"Classroom {classroom_id} not found")
    return class_obj.documents
