import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.asyncio
async def test_hello_world_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

@pytest.mark.asyncio
async def test_healthz_endpoint(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

### added test coverage for prime numbers
@pytest.mark.asyncio
async def test_primes_endpoint_valid_input(client):
    response = client.get("/primes/5")
    assert response.status_code == 200
    assert response.json() == {"count": 5, "primes": [2, 3, 5, 7, 11]}

@pytest.mark.asyncio
async def test_primes_endpoint_invalid_input(client):
    response = client.get("/primes/0")
    assert response.status_code == 400
    assert response.json() == {"detail": "Parameter n must be a positive integer"}    