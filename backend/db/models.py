import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)


class Class(Base):
    __tablename__ = "classes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_url: Mapped[str] = mapped_column(String(255), nullable=False)


# join table between classes and users
class ClassMembers(Base):
    __tablename__ = "class_members"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    class_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("classes.id"), primary_key=True
    )


# join table between classes and documents
class ClassDocuments(Base):
    __tablename__ = "class_documents"

    class_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("classes.id"), primary_key=True
    )
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("documents.id"))
