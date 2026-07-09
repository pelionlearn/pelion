from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models.base import Base

if TYPE_CHECKING:
    from api.models.classroom import Classroom


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str]

    password_hash: Mapped[str]

    owned_classes: Mapped[list["Classroom"]] = relationship(
        back_populates="owner",
        foreign_keys="Classroom.owner_id"
    )

    classrooms: Mapped[list["Classroom"]] = relationship(
        secondary="classroom_members",
        back_populates="members"
    )