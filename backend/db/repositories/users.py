from db.database import Session
from db.models import User


def create_user(name: str, email: str):
    with Session() as session:
        user = User(name, email)

        session.add(user)
        session.commit()
        session.refresh(user)

        return user


def get_users():
    with Session() as session:
        return session.query(User).all()
