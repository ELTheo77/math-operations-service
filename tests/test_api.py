"""API endpoint tests."""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models.schemas import OperationType


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


@pytest.mark.asyncio
async def test_calculate_power():
    """Test power calculation."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/calculate",
            json={
                "operation": "power",
                "value": 2,
                "exponent": 10
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 1024
        assert data["operation"] == "power"
        assert data["input_value"] == 2
        assert data["exponent"] == 10


@pytest.mark.asyncio
async def test_calculate_fibonacci():
    """Test Fibonacci calculation."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/calculate",
            json={
                "operation": "fibonacci",
                "value": 10
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 55
        assert data["operation"] == "fibonacci"
        assert data["input_value"] == 10


@pytest.mark.asyncio
async def test_calculate_factorial():
    """Test factorial calculation."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/calculate",
            json={
                "operation": "factorial",
                "value": 5
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 120
        assert data["operation"] == "factorial"
        assert data["input_value"] == 5


@pytest.mark.asyncio
async def test_invalid_operation():
    """Test invalid operation handling."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/calculate",
            json={
                "operation": "invalid",
                "value": 5
            }
        )
        assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_negative_factorial():
    """Test factorial with negative number."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/calculate",
            json={
                "operation": "factorial",
                "value": -5
            }
        )
        assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_cache_hit():
    """Test that cached results are returned."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First request
        response1 = await client.post(
            "/api/v1/calculate",
            json={
                "operation": "fibonacci",
                "value": 20
            }
        )
        assert response1.status_code == 200
        data1 = response1.json()
        assert data1["cached"] is False
        
        # Second request (should be cached)
        response2 = await client.post(
            "/api/v1/calculate",
            json={
                "operation": "fibonacci",
                "value": 20
            }
        )
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["cached"] is True
        assert data2["result"] == data1["result"]
        assert data2["computation_time_ms"] == 0.0