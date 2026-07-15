from sqlalchemy.orm import Session
from db.models import Classroom
from uuid import UUID
from exceptions import errors


def create_classroom(db: Session, name: str):
    obj = Classroom(name=name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_classroom(db: Session, id: UUID):
    obj = db.get(Classroom, id)
    if obj is None:
        raise errors.NotFoundError(f"Classroom {id} not found")
    db.delete(obj)
    db.commit()
    return obj


def get_classroom(db: Session, id: UUID):
    obj = db.get(Classroom, id)
    if obj is None:
        raise errors.NotFoundError(f"Classroom {id} not found")
    return obj


def rename_classroom(db: Session, id: UUID, name: str):
    class_obj = db.get(Classroom, id)

    if class_obj is None:
        raise errors.NotFoundError(f"Classroom {id} not found")

    class_obj.name = name

    db.commit()
    db.refresh(class_obj)

    return class_obj
