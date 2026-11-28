from uuid import UUID
from tests.conftest import as_user
from tests.api.support.factories import create_classroom


MISSING_USER_ID = "00000000-0000-0000-0000-000000000000"

class TestCurrentUser:
    async def test_get_me(self, client, user):
        response = await client.get("/users/me", headers=as_user(user))

        assert response.status_code == 200

        body = response.json()

        assert UUID(body["id"]) == user.id
        assert body["email"] == user.email
        assert body["name"] == user.name

    async def test_update_me(self, client, user):
        response = await client.patch(
            "/users/me",
            json={"name": "DifferentUser"},
            headers=as_user(user)
        )

        assert response.status_code == 200
        assert response.json()["name"] == "DifferentUser"

    async def test_get_me_classrooms(self, client, user):
        create_response = await create_classroom(client, user, name="Physics")

        assert create_response.status_code == 200
        classroom_id = create_response.json()["id"]

        response = await client.get("/users/me/classrooms", headers=as_user(user))

        assert response.status_code == 200

        classrooms = response.json()

        assert len(classrooms) == 1
        assert classrooms[0]["id"] == classroom_id
        assert classrooms[0]["name"] == "Physics"

class TestGetUser:
    async def test_get_another_user(self, client, user, outsider):
        response = await client.get(f"/users/{outsider.id}", headers=as_user(user))

        assert response.status_code == 200

        body = response.json()

        assert body["id"] == str(outsider.id)
        assert body["email"] == outsider.email

    async def test_get_missing_user(self, client, user):
        response = await client.get(f"/users/{MISSING_USER_ID}", headers=as_user(user))

        assert response.status_code == 404

    async def test_invalid_uuid(self, client, user):
        response = await client.get("/users/asdfj12345", headers=as_user(user))

        assert response.status_code == 422  # unprocessable entity

class TestAuthorization:
    async def test_get_me_requires_auth(self, client):
        response = await client.get("/users/me")
        assert response.status_code == 401

    async def test_get_user_requires_auth(self, client, outsider):
        response = await client.get(f"/users/{outsider.id}")
        assert response.status_code == 401