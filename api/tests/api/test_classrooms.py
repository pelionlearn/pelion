from uuid import UUID


async def test_create_classroom(client):

    response = await client.post("/classrooms/", json={"name": "Calculus 1"})

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "Calculus 1"
    assert "id" in body

    # verify UUID format
    UUID(body["id"])


async def test_get_classroom(client):

    # create classroom first
    create_response = await client.post("/classrooms/", json={"name": "Physics"})

    assert create_response.status_code == 200

    classroom_id = create_response.json()["id"]

    # retrieve classroom
    response = await client.get(f"/classrooms/{classroom_id}")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == classroom_id
    assert body["name"] == "Physics"


async def test_delete_classroom(client):

    create_response = await client.post("/classrooms/", json={"name": "Drama"})

    classroom_id = create_response.json()["id"]

    response = await client.delete(f"/classrooms/{classroom_id}")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == classroom_id


async def test_get_missing_classroom(client):

    response = await client.get("/classrooms/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404


async def test_invalid_uuid(client):

    response = await client.get("/classrooms/asdfj12345")

    assert response.status_code == 422  # unproccesable entity


async def test_invalid_schema(client):
    response = await client.post("/classrooms/", json={"member": "Jawsh"})

    assert response.status_code == 422
