import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from main import app
from db.base import Base
from db.database import engine, get_db
from auth.authentication import current_active_user
from fastapi import Request, HTTPException
from uuid import UUID

### SESSION AND CLIENT FIXTURES

@pytest.fixture
async def db_session():
    # use the engine and connection from db.database
    async with engine.connect() as connection:
        # start a transaction for this test so we can rollback later
        transaction = await connection.begin()

        # new session bound to the db.database engine connection
        session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
        )

        try:
            yield session
        finally:
            await session.close()
            await transaction.rollback()


@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    async def override_user(request: Request) -> User:
        raw_id = request.headers.get("X-Test-User")
        if raw_id is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        current = await db_session.get(User, UUID(raw_id))
        if current is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return current

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[current_active_user] = override_user

    try:
        async with AsyncClient(
            transport=ASGITransport(app), base_url="http://test", follow_redirects=True
        ) as client:
            yield client
    finally:
        app.dependency_overrides.clear()

async def make_user(db_session, email, name):
    user = User(email=email, name=name, hashed_password="unnecessary", is_active=True, is_verified=True)
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)
    return user

@pytest.fixture
async def user(db_session):
    return await make_user(db_session, "user@example.com", "Owner")

@pytest.fixture
async def outsider(db_session):
    return await make_user(db_session, "outsider@example.com", "Outsider")

def as_user(user):
    return {"X-Test-User": str(user.id)}


# OBJECT FIXTURES

# @pytest.fixture
# async def classroom_factory(client, user):
#     async def factory(name="Computer Science", color="#00FF00"):
#         response = await client.post(
#             "/classrooms/", json={"name": name, "color": color},
#             headers=as_user(user)
#         )
#         return response
#     return factory

# @pytest.fixture
# async def user_factory(client):
#     async def factory(email="jane@example.com", password="hunter2hunter2", name="Jane Doe"):
#         response = await client.post(
#             "/auth/register/",
#             json={
#                 "email": email,
#                 "password": password,
#                 "name": name,
#             },
#         )
#         return response
#     return factory

# @pytest.fixture
# async def document_factory(authenticated_client):
#     async def factory(classroom_id, filename):
#         response = await authenticated_client.post(
#             "/classrooms/", json={"name": "Calculus 1", "color": "#FF0000"}
#         )
#         return response

#     return factory


### OBJECT HELPERS

# async def create_classroom(authenticated_client, classroom_factory):

#     response = await classroom_factory()

#     assert response.status_code == 200
#     assert "id" in response.json()

#     classroom_id = response.json()["id"]

#     members_response = await authenticated_client.get(
#         f"/classrooms/{classroom_id}/users"
#     )

#     assert members_response.status_code == 200
#     assert len(members_response.json()) == 1

#     return classroom_id


# async def create_user(user_factory):
#     response = await user_factory()

#     assert response.status_code == 201

#     return response.json()["id"]
