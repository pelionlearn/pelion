import asyncio

# required for psycopg async on Windows
asyncio.set_event_loop_policy(
    asyncio.WindowsSelectorEventLoopPolicy()
)

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.database import engine, SessionLocal
from api.models.base import Base
from api.models.user import User
from api.models.classroom import Classroom, ClassroomMember


async def main():
    # create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        # create user
        user = User(
            email="teacher@test.com",
            password_hash="test_hash"
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        print(f"Created user: {user.id}")

        # create classroom
        classroom = Classroom(
            name="Physics",
            owner_id=user.id
        )

        db.add(classroom)
        await db.commit()
        await db.refresh(classroom)

        print(f"Created classroom: {classroom.id}")

        # add user as classroom member
        member = ClassroomMember(
            classroom_id=classroom.id,
            user_id=user.id,
            role="owner"
        )

        db.add(member)
        await db.commit()

        print("Added member")

        # query classrooms with relationships loaded
        result = await db.execute(
            select(Classroom)
            .options(
                selectinload(Classroom.members),
                selectinload(Classroom.owner)
            )
        )

        classrooms = result.scalars().all()

        for classroom in classrooms:
            print("\nClassroom:")
            print("ID:", classroom.id)
            print("Name:", classroom.name)

            print("Owner:")
            print(classroom.owner.email)

            print("Members:")
            for member in classroom.members:
                print(
                    f"- {member.email}"
                )


if __name__ == "__main__":
    asyncio.run(main())