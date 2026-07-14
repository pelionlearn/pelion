from db.database import Session
from db.models import User
from exceptions import errors


def create_user(name: str, email: str):
    with Session() as session:
        user = User(name=name, email=email)

        session.add(user)
        session.commit()
        session.refresh(user)

        return user


def delete_user(id):
    with Session() as session:
        user = session.get(User, id)
        if user is None:
            raise errors.NotFoundError(f"User {id} not found")
        session.delete(user)
        session.commit()
        return user


def get_user(id):
    with Session() as session:
        user = session.get(User, id)
        if user is None:
            raise errors.NotFoundError(f"User {id} not found")
        return user


def get_all_users():
    with Session() as session:
        return session.query(User).all()


def rename_user(id, name: str):
    with Session() as session:
        user = session.get(User, id)

        if user is None:
            raise errors.NotFoundError(f"User {id} not found")

        user.name = name

        session.commit()
        session.refresh(user)

        return user


def get_user_classes(id):
    with Session() as session:
        user = session.get(User, id)
        if user is None:
            raise errors.NotFoundError(f"User {id} not found")
        return user.classrooms
