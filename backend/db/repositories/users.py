from db.database import Session
from db.models import User


def create(name: str, email: str):
    with Session() as session:
        user = User(name=name, email=email)

        session.add(user)
        session.commit()
        session.refresh(user)

        return user


def delete(id):
    with Session() as session:
        user = session.get(User, id)
        if user:
            session.delete(user)
            session.commit()
            return user
        else:
            return None


def get(id):
    with Session() as session:
        user = session.get(User, id)
        return user


def get_all():
    with Session() as session:
        return session.query(User).all()


def rename(id, name: str):
    with Session() as session:
        user = session.get(User, id)

        if user is None:
            return None

        user.name = name

        session.commit()
        session.refresh(user)

        return user


def get_classes(id):
    with Session() as session:
        user = session.get(User, id)
        if user:
            return user.classes
        else:
            return None
