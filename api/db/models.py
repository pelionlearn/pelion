import uuid
from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from fastapi_users.db import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyBaseOAuthAccountTableUUID,
)
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    __tablename__ = "oauth_account"

    # override the "user.id" foreign key to "users.id"
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )


# stores server side session tokens
class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    __tablename__ = "access_token"

    # override the "user.id" foreign key to "users.id"
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    # id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    # email: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False, default="")

    classrooms: Mapped[list["Classroom"]] = relationship(
        secondary="classroom_members", back_populates="members", lazy="raise"
    )

    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount",
        lazy="selectin",
    )


class Classroom(Base):
    __tablename__ = "classrooms"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    members: Mapped[list["User"]] = relationship(
        secondary="classroom_members", back_populates="classrooms", lazy="raise"
    )
    documents: Mapped[list["Document"]] = relationship(
        back_populates="classroom", lazy="raise"
    )


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    content_type: Mapped[str | None] = mapped_column(nullable=True)
    size: Mapped[int] = mapped_column()

    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    classroom_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("classrooms.id"))

    # weird name bc i cant use class keyword, prob should rename to classroom
    classroom: Mapped["Classroom"] = relationship(
        back_populates="documents", lazy="raise"
    )


# join table between classrooms and users
class ClassroomMember(Base):
    __tablename__ = "classroom_members"

    classroom_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("classrooms.id"), primary_key=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
