"""Service layer tests."""
import pytest

from app.services.calculator import CalculatorService
from app.services.cache import CacheService


@pytest.mark.asyncio
async def test_power_calculation():
    """Test power calculation service."""
    calculator = CalculatorService()
    result, time_ms = await calculator.power(2, 10)
    assert result == 1024
    assert time_ms >= 0


@pytest.mark.asyncio
async def test_power_edge_cases():
    """Test power calculation edge cases."""
    calculator = CalculatorService()
    
    # Zero exponent
    result, _ = await calculator.power(5, 0)
    assert result == 1
    
    # Negative exponent
    result, _ = await calculator.power(2, -2)
    assert result == 0.25
    
    # Large numbers
    result, _ = await calculator.power(10, 10)
    assert result == 10000000000


@pytest.mark.asyncio
async def test_fibonacci_calculation():
    """Test Fibonacci calculation service."""
    calculator = CalculatorService()
    
    # Test known values
    test_cases = [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (10, 55),
        (15, 610)
    ]
    
    for n, expected in test_cases:
        result, time_ms = await calculator.fibonacci(n)
        assert result == expected
        assert time_ms >= 0


@pytest.mark.asyncio
async def test_factorial_calculation():
    """Test factorial calculation service."""
    calculator = CalculatorService()
    
    # Test known values
    test_cases = [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
        (6, 720),
        (10, 3628800)
    ]
    
    for n, expected in test_cases:
        result, time_ms = await calculator.factorial(n)
        assert result == expected
        assert time_ms >= 0


@pytest.mark.asyncio
async def test_factorial_negative():
    """Test factorial with negative input."""
    calculator = CalculatorService()
    
    with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
        await calculator.factorial(-5)


@pytest.mark.asyncio
async def test_cache_service():
    """Test cache service functionality."""
    cache = CacheService(max_size=3, ttl_seconds=60)
    
    # Test set and get
    await cache.set("power", 2, 1024, exponent=10)
    result = await cache.get("power", 2, exponent=10)
    assert result == 1024
    
    # Test cache miss
    result = await cache.get("power", 3, exponent=10)
    assert result is None
    
    # Test LRU eviction
    await cache.set("fibonacci", 10, 55)
    await cache.set("factorial", 5, 120)
    await cache.set("power", 3, 27, exponent=3)  # This should evict the oldest
    
    # Check cache size
    stats = await cache.get_stats()
    assert stats['size'] == 3
    
    # Clear cache
    await cache.clear()
    stats = await cache.get_stats()
    assert stats['size'] == 0