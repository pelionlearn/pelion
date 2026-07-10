from db.database import Session
from db.models import Document, ClassDocuments


def create(self, name, class_id):
    with Session() as session:
        obj = Document(name)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj


def delete(self, id):
    with Session() as session:
        obj = session.get(Document, id)
        if obj:
            session.delete(obj)
            session.commit()
        else:
            return None


def get(self, id):
    with Session() as session:
        obj = session.get(Document, id)
        return obj


def rename(self, id, name: str):
    with Session() as session:
        document = session.get(Document, id)

        if document is None:
            return None

        document.name = name

        session.commit()
        session.refresh(document)

        return document


def get_class(self, id):
    with Session() as session:
        document = session.get(Document, id)
        return document.class_
