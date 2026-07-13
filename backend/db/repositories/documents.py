from db.database import Session
from db.models import Document, Classroom
from uuid import UUID
from api.exceptions import errors


def create_document(file_name: str, file_url: str, classroom_id: UUID):
    with Session() as session:
        obj = Document(
            file_name=file_name, file_url=file_url, classroom_id=classroom_id
        )
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj


def delete_document(id):
    with Session() as session:
        obj = session.get(Document, id)
        if obj is None:
            raise errors.NotFoundError(f"Document {id} not found")
        session.delete(obj)
        session.commit()
        return obj


def get_document(id):
    with Session() as session:
        obj = session.get(Document, id)
        if obj is None:
            raise errors.NotFoundError(f"Document {id} not found")
        return obj


def rename_document(id, name: str):
    with Session() as session:
        document = session.get(Document, id)

        if document is None:
            raise errors.NotFoundError(f"Document {id} not found")

        document.file_name = name

        session.commit()
        session.refresh(document)

        return document


def get_document_class(id):
    with Session() as session:
        document = session.get(Document, id)
        if document is None:
            raise errors.NotFoundError(f"Document {id} not found")
        return document.classroom


def get_class_documents(classroom_id: UUID):
    with Session() as session:
        class_obj = session.get(Classroom, classroom_id)
        if class_obj is None:
            raise errors.NotFoundError(f"Classroom {classroom_id} not found")
        return class_obj.documents
