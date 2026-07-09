from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models.base import Base

if TYPE_CHECKING:
    from api.models.user import User


class ClassroomMember(Base):
    __tablename__ = "classroom_members"

    classroom_id: Mapped[int] = mapped_column(
        ForeignKey("classes.id"),
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )

    role: Mapped[str] = mapped_column(
        String(50),
        default="student"
    )


class Classroom(Base):
    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    owner: Mapped["User"] = relationship(
        back_populates="owned_classes",
        foreign_keys=[owner_id]
    )

    members: Mapped[list["User"]] = relationship(
        secondary="classroom_members",
        back_populates="classrooms"
    )