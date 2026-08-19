from uuid import UUID


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


async def create_document(
    authenticated_client, classroom_id, filename, content=b"test file"
):
    response = await authenticated_client.post(
        f"/classrooms/{classroom_id}/documents/",
        files={
            "file": (
                filename,
                content,
                "application/pdf",
            )
        },
    )

    return response


async def test_create_document(authenticated_client):

    classroom_id = await create_classroom(authenticated_client)

    response = await create_document(
        authenticated_client, classroom_id, "lecture1.pdf", content=b"fake pdf contents"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["file_name"] == "lecture1.pdf"
    assert body["content_type"] == "application/pdf"
    assert body["size"] == len(b"fake pdf contents")

    UUID(body["id"])


async def test_get_document(authenticated_client):

    classroom_id = await create_classroom(authenticated_client)

    create_response = await create_document(
        authenticated_client, classroom_id, "notes.pdf"
    )

    document_id = create_response.json()["id"]

    response = await authenticated_client.get(
        f"/classrooms/{classroom_id}/documents/{document_id}"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == document_id
    assert body["file_name"] == "notes.pdf"


async def test_get_class_documents(authenticated_client):

    classroom_id = await create_classroom(authenticated_client)

    await create_document(
        authenticated_client,
        classroom_id,
        "chapter1.pdf",
        content=b"This is a boring textbook",
    )
    await create_document(
        authenticated_client,
        classroom_id,
        "chapter1.pdf",
        content=b"This is a boring textbook",
    )

    response = await authenticated_client.get(f"/classrooms/{classroom_id}/documents/")

    assert response.status_code == 200

    documents = response.json()

    assert len(documents) == 2


async def test_delete_document(authenticated_client):

    classroom_id = await create_classroom(authenticated_client)

    create_response = await create_document(
        authenticated_client,
        classroom_id,
        "delete_me.pdf",
        content=b"Please delete me. This world is too painful",
    )

    document_id = create_response.json()["id"]

    response = await authenticated_client.delete(
        f"/classrooms/{classroom_id}/documents/{document_id}"
    )

    assert response.status_code == 200

    assert response.json()["id"] == document_id


async def test_add_missing_class_documents(authenticated_client):

    response = await create_document(
        authenticated_client, "00000000-0000-0000-0000-000000000000", "chapter1.pdf"
    )

    assert response.status_code == 403


async def test_get_missing_class_documents(authenticated_client):

    response = await authenticated_client.get(
        "/classrooms/00000000-0000-0000-0000-000000000000/documents/"
    )

    assert response.status_code == 403


async def test_delete_missing_class_documents(authenticated_client):
    classroom_id = await create_classroom(authenticated_client)

    response = await authenticated_client.delete(
        f"/classrooms/{classroom_id}/documents/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404


async def test_invalid_uuid(authenticated_client):
    classroom_id = await create_classroom(authenticated_client)

    response = await authenticated_client.get(
        f"/classrooms/{classroom_id}/documents/asdfj12345"
    )

    assert response.status_code == 422  # unproccesable entity


async def test_invalid_schema(authenticated_client):
    classroom_id = await create_classroom(authenticated_client)

    response = await authenticated_client.post(
        f"/classrooms/{classroom_id}/documents", json={"file_name": "amogus"}
    )

    assert response.status_code == 422
