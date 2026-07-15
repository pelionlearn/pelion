from sqlalchemy.orm import Session
from db.models import User
from exceptions import errors


def create_user(db: Session, name: str, email: str):
    user = User(name=name, email=email)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, id):
    user = db.get(User, id)
    if user is None:
        raise errors.NotFoundError(f"User {id} not found")
    db.delete(user)
    db.commit()
    return user


def get_user(db: Session, id):
    user = db.get(User, id)
    if user is None:
        raise errors.NotFoundError(f"User {id} not found")
    return user


def get_all_users(db: Session):
    return db.query(User).all()


def rename_user(db: Session, id, name: str):
    user = db.get(User, id)

    if user is None:
        raise errors.NotFoundError(f"User {id} not found")

    user.name = name

    db.commit()
    db.refresh(user)

    return user


def get_user_classes(db: Session, id):
    user = db.get(User, id)
    if user is None:
        raise errors.NotFoundError(f"User {id} not found")
    return user.classrooms
