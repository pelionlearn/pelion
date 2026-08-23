async def create_classroom(authenticated_client):

    response = await authenticated_client.post(
        "/classrooms/", json={"name": "Computer Science"}
    )

    assert response.status_code == 200
    assert "id" in response.json()

    classroom_id = response.json()["id"]

    members_response = await authenticated_client.get(
        f"/classrooms/{classroom_id}/users"
    )

    assert members_response.status_code == 200
    assert len(members_response.json()) == 1

    return classroom_id


async def create_user(authenticated_client):
    response = await authenticated_client.post(
        "/auth/register/",
        json={
            "email": "jane@example.com",
            "password": "hunter2hunter2",
            "name": "Jane Doe",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


async def test_add_member(authenticated_client):
    classroom_id = await create_classroom(authenticated_client)
    user_id = await create_user(authenticated_client)

    response = await authenticated_client.post(
        f"/classrooms/{classroom_id}/users/{user_id}"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == user_id
    assert body["name"] == "Jane Doe"
    assert body["email"] == "jane@example.com"


async def test_get_classroom_members(authenticated_client):
    classroom_id = await create_classroom(authenticated_client)
    user_id = await create_user(authenticated_client)

    await authenticated_client.post(f"/classrooms/{classroom_id}/users/{user_id}")

    response = await authenticated_client.get(f"/classrooms/{classroom_id}/users/")

    assert response.status_code == 200

    members = response.json()

    # 2 members bc creator is automatically a member
    assert len(members) == 2
    assert members[1]["id"] == user_id


async def test_remove_member(authenticated_client):
    classroom_id = await create_classroom(authenticated_client)
    user_id = await create_user(authenticated_client)

    add_response = await authenticated_client.post(
        f"/classrooms/{classroom_id}/users/{user_id}"
    )
    assert add_response.status_code == 200

    members_response = await authenticated_client.get(
        f"/classrooms/{classroom_id}/users/"
    )
    assert members_response.status_code == 200
    assert len(members_response.json()) == 2  # now 2 members, including creator

    delete_response = await authenticated_client.delete(
        f"/classrooms/{classroom_id}/users/{user_id}"
    )
    assert delete_response.status_code == 200

    members_response = await authenticated_client.get(
        f"/classrooms/{classroom_id}/users/"
    )
    assert members_response.status_code == 200
    assert len(members_response.json()) == 1  # back to just the creator


async def test_get_members_missing_classroom(authenticated_client):
    response = await authenticated_client.get(
        "/classrooms/00000000-0000-0000-0000-000000000000/users/"
    )

    # client shouldnt know whether classroom exists or not if they arent in it
    assert response.status_code == 404


async def test_remove_missing_member(authenticated_client):
    classroom_id = await create_classroom(authenticated_client)
    user_id = await create_user(authenticated_client)

    response = await authenticated_client.delete(
        f"/classrooms/{classroom_id}/users/{user_id}"
    )

    assert response.status_code == 404
