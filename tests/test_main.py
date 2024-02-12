import pytest
from httpx import AsyncClient
from main import app  # Import your FastAPI app

# Use pytest-asyncio for async test functions
@pytest.mark.asyncio
async def test_register_device():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/Device/register", json={"userKey": "user123", "deviceType": "Android"})
    assert response.status_code == 200
    assert response.json() == {"statusCode": 200, "message": "Device registered successfully"}

@pytest.mark.asyncio
async def test_store_user_login_event():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/Log/auth", json={"userKey": "user123", "deviceType": "Android"})
    assert response.status_code == 200
    assert response.json() == {"statusCode": 200, "message": "success"}

@pytest.mark.asyncio
async def test_get_device_statistics():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Assuming there's already a device registered from the previous test
        response = await ac.get("/Log/auth/statistics")
    assert response.status_code == 200
    # The exact assertion here will depend on the state of your database
    # This is just an example assuming the above tests have run
    assert any(item["deviceType"] == "Android" for item in response.json())

# Additional tests can be written to cover more scenarios, error cases, and input validation