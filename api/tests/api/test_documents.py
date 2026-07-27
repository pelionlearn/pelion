from uuid import UUID


def create_classroom(client):

    response = client.post("/classrooms/", json={"name": "Computer Science"})

    assert response.status_code == 200

    return response.json()["id"]


def test_create_document(client):

    classroom_id = create_classroom(client)

    response = client.post(
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


def test_get_document(client):

    classroom_id = create_classroom(client)

    create_response = client.post(
        f"/classrooms/{classroom_id}/documents/",
        json={
            "file_name": "notes.pdf",
            "file_url": "https://example.com/notes.pdf",
        },
    )

    document_id = create_response.json()["id"]

    response = client.get(f"/classrooms/{classroom_id}/documents/{document_id}")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == document_id
    assert body["file_name"] == "notes.pdf"


def test_get_class_documents(client):

    classroom_id = create_classroom(client)

    client.post(
        f"/classrooms/{classroom_id}/documents/",
        json={
            "file_name": "chapter1.pdf",
            "file_url": "https://example.com/chapter1.pdf",
        },
    )

    client.post(
        f"/classrooms/{classroom_id}/documents/",
        json={
            "file_name": "chapter2.pdf",
            "file_url": "https://example.com/chapter2.pdf",
        },
    )

    response = client.get(f"/classrooms/{classroom_id}/documents/")

    assert response.status_code == 200

    documents = response.json()

    assert len(documents) == 2


def test_delete_document(client):

    classroom_id = create_classroom(client)

    create_response = client.post(
        f"/classrooms/{classroom_id}/documents/",
        json={
            "file_name": "delete_me.pdf",
            "file_url": "https://example.com/delete.pdf",
        },
    )

    document_id = create_response.json()["id"]

    response = client.delete(f"/classrooms/{classroom_id}/documents/{document_id}")

    assert response.status_code == 200

    assert response.json()["id"] == document_id
