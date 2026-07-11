from db.database import Session
from db.models import Class, ClassMember
from uuid import UUID


def create(name: str):
    with Session() as session:
        obj = Class(name=name)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj


def delete(id: UUID):
    with Session() as session:
        obj = session.get(Class, id)
        if obj:
            session.delete(obj)
            session.commit()
            return obj
        else:
            return None


def get(id: UUID):
    with Session() as session:
        obj = session.get(Class, id)
        return obj


def rename(id: UUID, name: str):
    with Session() as session:
        class_obj = session.get(Class, id)

        if class_obj is None:
            return None

        class_obj.name = name

        session.commit()
        session.refresh(class_obj)

        return class_obj
