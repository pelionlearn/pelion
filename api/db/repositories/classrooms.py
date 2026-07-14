from db.database import Session
from db.models import Classroom
from uuid import UUID
from exceptions import errors


def create_classroom(name: str):
    with Session() as session:
        obj = Classroom(name=name)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj


def delete_classroom(id: UUID):
    with Session() as session:
        obj = session.get(Classroom, id)
        if obj is None:
            raise errors.NotFoundError(f"Classroom {id} not found")
        session.delete(obj)
        session.commit()
        return obj


def get_classroom(id: UUID):
    with Session() as session:
        obj = session.get(Classroom, id)
        if obj is None:
            raise errors.NotFoundError(f"Classroom {id} not found")
        return obj


def rename_classroom(id: UUID, name: str):
    with Session() as session:
        class_obj = session.get(Classroom, id)

        if class_obj is None:
            raise errors.NotFoundError(f"Classroom {id} not found")

        class_obj.name = name

        session.commit()
        session.refresh(class_obj)

        return class_obj
