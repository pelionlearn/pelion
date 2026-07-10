from db.database import Session
from db.models import Class, ClassMembers, User, ClassDocuments, Document
from uuid import UUID
from sqlalchemy import select


class ClassRepository:
    def create(self, name: str):
        with Session() as session:
            obj = Class(name)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def delete(self, id: UUID):
        with Session as session:
            obj = session.get(Class, id)
            if obj:
                session.delete(obj)
                session.commit()
            else:
                return None

    def get(self, id: UUID):
        with Session as session:
            obj = session.get(Class, id)
            return obj

    def rename(self, id: UUID, name: str):
        with Session() as session:
            class_obj = session.get(Class, id)

            if class_obj is None:
                return None

            class_obj.name = name

            session.commit()
            session.refresh(class_obj)

            return class_obj

    def get_members(self, class_id: UUID):
        with Session() as session:
            return session.scalars(
                select(User).join(ClassMembers).where(ClassMembers.class_id == class_id)
            )

    def get_documents(self, class_id: UUID):
        with Session() as session:
            return session.scalars(
                select(Document)
                .join(ClassDocuments)
                .where(ClassDocuments.class_id == class_id)
            )
