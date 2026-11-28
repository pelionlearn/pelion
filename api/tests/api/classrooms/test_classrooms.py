from uuid import UUID
import pytest
from tests.conftest import as_user
from tests.api.support.factories import create_classroom

MISSING_CLASSROOM_ID = "00000000-0000-0000-0000-000000000000"

class TestCreateClassroom:
    async def test_create(self, client, user):
        response = await create_classroom(
            client, user, name="Calc 1", color="#FF0000"
        )
        assert response.status_code == 200
        body = response.json()

        assert "id" in body
        UUID(body["id"])

        assert body["name"] == "Calc 1"
        assert body["color"] == "#FF0000"
        assert body["owner"] == str(user.id)

class TestGetClassroom:
    async def test_owner_can_get(self, client, user):
        classroom = (await create_classroom(client, user)).json()

        response = await client.get(
            f"/classrooms/{classroom["id"]}", headers=as_user(user)
        )

        assert response.status_code == 200
        assert response.json() == classroom

    async def test_missing_classroom_404(self, client, user):
        response = await client.get(
            f"/classrooms/{MISSING_CLASSROOM_ID}", headers=as_user(user)
        )

        assert response.status_code == 404

    async def test_non_member_404(self, client, user, outsider):
        classroom = (await create_classroom(client, user)).json()
        
        response = await client.get(
            f"/classrooms/{classroom["id"]}", headers=as_user(outsider)
        )

        # membership failures are 404 not 403, in order to hide existence of a classroom
        assert response.status_code == 404

class TestDeleteClassroom:
    async def test_owner_can_delete(self, client, user):
        classroom = (await create_classroom(client, user)).json()
        assert classroom["owner"] == str(user.id)

        response = await client.delete(
            f"/classrooms/{classroom["id"]}", headers=as_user(user)
        )

        assert response.status_code == 200

        # only write follow ups for endpoints (like DELETE) that arent required to return the resource
        follow_up = await client.get(f"/classrooms/{classroom["id"]}", headers=as_user(user))
        assert follow_up.status_code == 404

    async def test_non_owner_cannot_delete(self, client, user, outsider):
        classroom = (await create_classroom(client, user)).json()
        response = await client.delete(
            f"/classrooms/{classroom["id"]}", headers=as_user(outsider)
        )

        assert response.status_code == 403

class TestValidation:
    @pytest.mark.parametrize(
        "path",
        ["/classrooms/asdfj12345", "/classrooms/00000000-0000-0000-0000-00"]
    )
    async def test_invalid_uuid(self, client, user, path):
        response = await client.get(
            path, headers=as_user(user)
        )
        assert response.status_code == 422

    @pytest.mark.parametrize(
        "payload",
        [
            {"member": "Jawsh"},  # Missing required fields
            {"color": "#FF0000"},  # Missing name
            {"name": 123, "color": "#FF0000"},  # Invalid name type
            {"name": "Biology", "color": 123},  # Invalid color type
        ],
    )
    async def test_invalid_schema(self,client, user, payload):
        response = await client.post("/classrooms/", json=payload, headers=as_user(user))

        assert response.status_code == 422

    @pytest.mark.parametrize("color", ["#000FF", "F0000FF", "#9I02GL"])
    async def test_invalid_color(self, client, user, color):
        response = await create_classroom(client, user, name="Biology", color=color)

        assert response.status_code == 422