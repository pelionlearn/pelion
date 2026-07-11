import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    classrooms: Mapped[list["Class"]] = relationship(
        secondary="classroom_members", back_populates="members"
    )


class Class(Base):
    __tablename__ = "classrooms"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    members: Mapped[list["User"]] = relationship(
        secondary="classroom_members", back_populates="classrooms"
    )
    documents: Mapped[list["Document"]] = relationship(back_populates="classroom")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_url: Mapped[str] = mapped_column(String(255), nullable=False)

    classroom_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("classrooms.id"))

    # weird name bc i cant use class keyword, prob should rename to classroom
    classroom: Mapped["Class"] = relationship(back_populates="documents")


# join table between classrooms and users
class ClassMember(Base):
    __tablename__ = "classroom_members"

    classroom_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("classrooms.id"), primary_key=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
