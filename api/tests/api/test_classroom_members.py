async def create_classroom(client):
    response = await client.post("/classrooms/", json={"name": "Calculus 1"})

    assert response.status_code == 200
    assert "id" in response.json()

    return response.json()["id"]


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


async def test_add_member(client):
    classroom_id = await create_classroom(client)
    user_id = await create_user(client)

    response = await client.post(f"/classrooms/{classroom_id}/users/{user_id}")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == user_id
    assert body["name"] == "Jane Doe"
    assert body["email"] == "jane@example.com"


async def test_get_classroom_members(client):
    classroom_id = await create_classroom(client)
    user_id = await create_user(client)

    await client.post(f"/classrooms/{classroom_id}/users/{user_id}")

    response = await client.get(f"/classrooms/{classroom_id}/users/")

    assert response.status_code == 200

    members = response.json()

    assert len(members) == 1
    assert members[0]["id"] == user_id


async def test_get_empty_classroom_members(client):
    classroom_id = await create_classroom(client)

    response = await client.get(f"/classrooms/{classroom_id}/users/")

    assert response.status_code == 200
    assert response.json() == []


async def test_remove_member(client):
    classroom_id = await create_classroom(client)
    user_id = await create_user(client)

    await client.post(f"/classrooms/{classroom_id}/users/{user_id}")

    response = await client.delete(f"/classrooms/{classroom_id}/users/{user_id}")

    assert response.status_code == 200

    # member removed from classroom
    members_response = await client.get(f"/classrooms/{classroom_id}/users/")

    assert members_response.status_code == 200
    assert members_response.json() == []


async def test_get_members_missing_classroom(client):
    response = await client.get(
        "/classrooms/00000000-0000-0000-0000-000000000000/users/"
    )

    assert response.status_code == 404


async def test_remove_missing_member(client):
    classroom_id = await create_classroom(client)
    user_id = await create_user(client)

    response = await client.delete(f"/classrooms/{classroom_id}/users/{user_id}")

    assert response.status_code == 404
