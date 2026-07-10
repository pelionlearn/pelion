from db.database import Session
from db.models import User


class UserRepository:
    def create(self, name: str, email: str):
        with Session() as session:
            user = User(name, email)

            session.add(user)
            session.commit()
            session.refresh(user)

            return user

    def delete(self, id):
        with Session as session:
            user = session.get(User, id)
            if user:
                session.delete(user)
                session.commit()
            else:
                return None

    def get(self, id):
        with Session as session:
            user = session.get(User, id)
            return user

    def get_all(self):
        with Session() as session:
            return session.query(User).all()

    def rename(self, id, name: str):
        with Session() as session:
            user = session.get(User, id)

            if user is None:
                return None

            user.name = name

            session.commit()
            session.refresh(user)

            return user
