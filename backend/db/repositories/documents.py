from db.database import Session
from db.models import Document, Class
from uuid import UUID


def create(file_name: str, file_url: str, class_id: UUID):
    with Session() as session:
        obj = Document(file_name=file_name, file_url=file_url, class_id=class_id)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj


def delete(id):
    with Session() as session:
        obj = session.get(Document, id)
        if obj:
            session.delete(obj)
            session.commit()
            return obj
        else:
            return None


def get(id):
    with Session() as session:
        obj = session.get(Document, id)
        return obj


def rename(id, name: str):
    with Session() as session:
        document = session.get(Document, id)

        if document is None:
            return None

        document.file_name = name

        session.commit()
        session.refresh(document)

        return document


def get_class(id):
    with Session() as session:
        document = session.get(Document, id)
        if document is None:
            raise Exception
        return document.classroom


def get_documents(class_id: UUID):
    with Session() as session:
        class_obj = session.get(Class, class_id)
        if class_obj is None:
            raise Exception
        return class_obj.documents
