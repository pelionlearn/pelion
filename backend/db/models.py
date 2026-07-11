import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    classes: Mapped[list["Class"]] = relationship(
        secondary="class_members", back_populates="members"
    )


class Class(Base):
    __tablename__ = "classes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    members: Mapped[list["User"]] = relationship(
        secondary="class_members", back_populates="classes"
    )
    documents: Mapped[list["Document"]] = relationship(back_populates="class_")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_url: Mapped[str] = mapped_column(String(255), nullable=False)

    class_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("classes.id"))

    # weird name bc i cant use class keyword, prob should rename to classroom
    class_: Mapped["Class"] = relationship(back_populates="documents")


# join table between classes and users
class ClassMembers(Base):
    __tablename__ = "class_members"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    class_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("classes.id"), primary_key=True
    )
