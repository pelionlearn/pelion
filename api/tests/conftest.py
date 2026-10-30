import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from main import app
from db.base import Base
from db.database import engine, get_db
from auth.authentication import current_active_user

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

        yield session

        await session.close()
        await transaction.rollback()


@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test", follow_redirects=True
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def user(db_session):
    user = User(
        email="user@example.com",
        name="User",
        hashed_password="...",
        is_active=True,
        is_superuser=False,
        is_verified=True,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    return user


@pytest.fixture
async def authenticated_client(client, user):
    async def override_current_active_user():
        return user

    app.dependency_overrides[current_active_user] = override_current_active_user

    yield client

    app.dependency_overrides.pop(current_active_user, None)


# OBJECT FIXTURES

@pytest.fixture
async def classroom_factory(authenticated_client):
    async def factory(name="Computer Science", color="#00FF00"):
        response = await authenticated_client.post(
            "/classrooms/", json={"name": name, "color": color}
        )
        return response
    return factory

@pytest.fixture
async def user_factory(client):
    async def factory(email="jane@example.com", password="hunter2hunter2", name="Jane Doe"):
        response = await client.post(
            "/auth/register/",
            json={
                "email": email,
                "password": password,
                "name": name,
            },
        )
        return response
    return factory

# @pytest.fixture
# async def document_factory(authenticated_client):
#     async def factory(classroom_id, filename):
#         response = await authenticated_client.post(
#             "/classrooms/", json={"name": "Calculus 1", "color": "#FF0000"}
#         )
#         return response

#     return factory


### OBJECT HELPERS