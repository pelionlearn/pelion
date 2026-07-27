from uuid import UUID


async def create_classroom(client):

    response = await client.post("/classrooms/", json={"name": "Computer Science"})

    assert response.status_code == 200
    assert "id" in response.json()

    return response.json()["id"]


async def test_create_document(client):

    classroom_id = await create_classroom(client)

    response = await client.post(
        f"/classrooms/{classroom_id}/documents/",
        json={
            "file_name": "lecture1.pdf",
            "file_url": "https://example.com/lecture1.pdf",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["file_name"] == "lecture1.pdf"
    assert body["file_url"] == "https://example.com/lecture1.pdf"

    UUID(body["id"])


async def test_get_document(client):

    classroom_id = await create_classroom(client)

    create_response = await client.post(
        f"/classrooms/{classroom_id}/documents/",
        json={
            "file_name": "notes.pdf",
            "file_url": "https://example.com/notes.pdf",
        },
    )

    document_id = create_response.json()["id"]

    response = await client.get(f"/classrooms/{classroom_id}/documents/{document_id}")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == document_id
    assert body["file_name"] == "notes.pdf"


async def test_get_class_documents(client):

    classroom_id = await create_classroom(client)

    await client.post(
        f"/classrooms/{classroom_id}/documents/",
        json={
            "file_name": "chapter1.pdf",
            "file_url": "https://example.com/chapter1.pdf",
        },
    )

    await client.post(
        f"/classrooms/{classroom_id}/documents/",
        json={
            "file_name": "chapter2.pdf",
            "file_url": "https://example.com/chapter2.pdf",
        },
    )

    response = await client.get(f"/classrooms/{classroom_id}/documents/")

    assert response.status_code == 200

    documents = response.json()

    assert len(documents) == 2


async def test_delete_document(client):

    classroom_id = await create_classroom(client)

    create_response = await client.post(
        f"/classrooms/{classroom_id}/documents/",
        json={
            "file_name": "delete_me.pdf",
            "file_url": "https://example.com/delete.pdf",
        },
    )

    document_id = create_response.json()["id"]

    response = await client.delete(
        f"/classrooms/{classroom_id}/documents/{document_id}"
    )

    assert response.status_code == 200

    assert response.json()["id"] == document_id


async def test_add_missing_class_documents(client):

    response = await client.post(
        "/classrooms/00000000-0000-0000-0000-000000000000/documents/",
        json={
            "file_name": "chapter1.pdf",
            "file_url": "https://example.com/chapter1.pdf",
        },
    )

    assert response.status_code == 404


async def test_get_missing_class_documents(client):

    response = await client.get(
        "/classrooms/00000000-0000-0000-0000-000000000000/documents/"
    )

    assert response.status_code == 404


async def test_delete_missing_class_documents(client):
    classroom_id = await create_classroom(client)

    response = await client.delete(
        f"/classrooms/{classroom_id}/documents/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404


async def test_invalid_uuid(client):
    classroom_id = await create_classroom(client)

    response = await client.get(f"/classrooms/{classroom_id}/documents/asdfj12345")

    assert response.status_code == 422  # unproccesable entity


async def test_invalid_schema(client):
    classroom_id = await create_classroom(client)

    response = await client.post(
        f"/classrooms/{classroom_id}/documents", json={"file_name": "amogus"}
    )

    assert response.status_code == 422
