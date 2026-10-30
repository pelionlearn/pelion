from uuid import UUID

### HELPERS

async def create_user(user_factory):
    response = await user_factory()

    assert response.status_code == 201

    return response.json()["id"]

### CRUD

async def test_get_me(authenticated_client, user):
    response = await authenticated_client.get("/users/me")

    assert response.status_code == 200

    body = response.json()

    assert UUID(body["id"]) == user.id

    assert body["email"] == user.email


async def test_get_user(authenticated_client, user_factory):
    other_user_id = await create_user(user_factory)

    response = await authenticated_client.get(f"/users/{other_user_id}")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == other_user_id


async def test_update_me(authenticated_client):
    response = await authenticated_client.patch(
        "/users/me", json={"name": "DifferentUser"}
    )

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "DifferentUser"

### SCOPE

async def test_auth_get_user(client, user_factory):
    other_user_id = await create_user(user_factory)

    response = await client.get(f"/users/{other_user_id}")

    assert response.status_code == 401 # Unauthorized bc not logged in
