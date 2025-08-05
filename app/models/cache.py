"""Simple in-memory caching service."""
import json
from datetime import datetime, timedelta
from typing import Optional, Any, Dict
import asyncio
from collections import OrderedDict


class CacheService:
    """Dictionary-based caching service with TTL support."""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        """
        Initialize cache service.
        
        Args:
            max_size: Maximum number of items in cache
            ttl_seconds: Time-to-live for cache entries in seconds
        """
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self._max_size = max_size
        self._ttl_seconds = ttl_seconds
        self._lock = asyncio.Lock()

    def _generate_key(self, operation: str, value: int, exponent: Optional[int] = None) -> str:
        """Generate cache key from operation parameters."""
        if exponent is not None:
            return f"{operation}:{value}:{exponent}"
        return f"{operation}:{value}"

    async def get(self, operation: str, value: int, exponent: Optional[int] = None) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            operation: Operation type
            value: Input value
            exponent: Optional exponent for power operation
            
        Returns:
            Cached result if found and not expired, None otherwise
        """
        key = self._generate_key(operation, value, exponent)
        
        async with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                # Check if entry is expired
                if datetime.utcnow() < entry['expires_at']:
                    # Move to end (LRU)
                    self._cache.move_to_end(key)
                    return entry['result']
                else:
                    # Remove expired entry
                    del self._cache[key]
        
        return None

    async def set(
        self,
        operation: str,
        value: int,
        result: Any,
        exponent: Optional[int] = None
    ) -> None:
        """
        Set value in cache.
        
        Args:
            operation: Operation type
            value: Input value
            result: Calculation result
            exponent: Optional exponent for power operation
        """
        key = self._generate_key(operation, value, exponent)
        
        async with self._lock:
            # Remove oldest entry if cache is full
            if len(self._cache) >= self._max_size and key not in self._cache:
                self._cache.popitem(last=False)
            
            # Add or update entry
            self._cache[key] = {
                'result': result,
                'expires_at': datetime.utcnow() + timedelta(seconds=self._ttl_seconds),
                'created_at': datetime.utcnow()
            }
            # Move to end (most recently used)
            self._cache.move_to_end(key)

    async def clear(self) -> None:
        """Clear all cache entries."""
        async with self._lock:
            self._cache.clear()

    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        async with self._lock:
            return {
                'size': len(self._cache),
                'max_size': self._max_size,
                'ttl_seconds': self._ttl_seconds,
                'entries': len(self._cache)
            }


# Global cache instance
cache_service = CacheService()