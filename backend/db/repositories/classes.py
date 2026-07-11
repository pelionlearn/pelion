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


def get_members(class_id: UUID):
    with Session() as session:
        class_obj = session.get(Class, class_id)
        return class_obj.members


def add_member(class_id: UUID, user_id: UUID):
    with Session() as session:
        class_member = ClassMember(class_id=class_id, user_id=user_id)
        session.add(class_member)
        session.commit()
        session.refresh(class_member)


def remove_member(class_id: UUID, user_id: UUID):
    with Session() as session:
        class_member = session.get(ClassMember, (class_id, user_id))
        if class_member:
            session.delete(class_member)
        else:
            return None


def get_documents(class_id: UUID):
    with Session() as session:
        class_obj = session.get(Class, class_id)
        return class_obj.documents
