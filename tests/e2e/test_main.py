import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_lifespan_triggers(asyn_test_client):
    response = await asyn_test_client.get("/healthy")
    assert response.status_code == 200


def test_health_check_endpoint(test_client):
    response = test_client.get("healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
