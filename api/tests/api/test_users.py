from uuid import UUID


async def create_user(client):
    response = await client.post(
        "/auth/register/",
        json={
            "email": "jane@example.com",
            "password": "hunter2hunter2",
            "name": "Jane Doe",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


async def test_get_me(authenticated_client, user):
    response = await authenticated_client.get("/users/me")

    assert response.status_code == 200

    body = response.json()

    assert UUID(body["id"]) == user.id

    assert body["email"] == user.email


async def test_get_user(authenticated_client, client):
    other_user_id = await create_user(client)

    response = await authenticated_client.get(f"/users/{other_user_id}")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == other_user_id


async def test_patch_me(authenticated_client):
    response = await authenticated_client.patch(
        "/users/me", json={"name": "DifferentUser"}
    )

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "DifferentUser"


async def test_auth_get_user(client):
    other_user_id = await create_user(client)

    response = await client.get(f"/users/{other_user_id}")

    assert response.status_code == 401
