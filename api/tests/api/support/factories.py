import pytest
from tests.conftest import as_user

async def create_classroom(client, user, name="Computer Science", color="#00FF00"):
    response = await client.post(
        "/classrooms/", json={"name": name, "color": color}, headers=as_user(user)
    )
    return response