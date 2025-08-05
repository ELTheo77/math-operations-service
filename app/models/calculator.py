"""Calculator service with mathematical operations."""
import asyncio
from functools import lru_cache
from typing import Tuple, Optional
import time


class CalculatorService:
    """Service for performing mathematical calculations."""

    @staticmethod
    async def power(base: int, exponent: int) -> Tuple[int, float]:
        """
        Calculate base raised to the power of exponent.
        
        Args:
            base: Base number
            exponent: Exponent
            
        Returns:
            Tuple of (result, computation_time_ms)
        """
        start_time = time.time()
        
        # Use Python's built-in pow for efficiency
        result = pow(base, exponent)
        
        computation_time = (time.time() - start_time) * 1000
        return result, computation_time

    @staticmethod
    async def fibonacci(n: int) -> Tuple[int, float]:
        """
        Calculate the n-th Fibonacci number using dynamic programming.
        
        Args:
            n: Position in Fibonacci sequence
            
        Returns:
            Tuple of (result, computation_time_ms)
        """
        start_time = time.time()
        
        if n <= 0:
            result = 0
        elif n == 1:
            result = 1
        else:
            # Dynamic programming approach for efficiency
            result = CalculatorService._fibonacci_dp(n)
        
        computation_time = (time.time() - start_time) * 1000
        return result, computation_time

    @staticmethod
    def _fibonacci_dp(n: int) -> int:
        """Dynamic programming implementation of Fibonacci."""
        if n <= 1:
            return n
        
        prev, curr = 0, 1
        for _ in range(2, n + 1):
            prev, curr = curr, prev + curr
        
        return curr

    @staticmethod
    async def factorial(n: int) -> Tuple[int, float]:
        """
        Calculate the factorial of n.
        
        Args:
            n: Non-negative integer
            
        Returns:
            Tuple of (result, computation_time_ms)
        """
        start_time = time.time()
        
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        
        result = CalculatorService._factorial_iterative(n)
        
        computation_time = (time.time() - start_time) * 1000
        return result, computation_time

    @staticmethod
    def _factorial_iterative(n: int) -> int:
        """Iterative implementation of factorial."""
        if n <= 1:
            return 1
        
        result = 1
        for i in range(2, n + 1):
            result *= i
        
        return result


class AsyncCalculatorService(CalculatorService):
    """
    Async calculator service with support for concurrent operations.
    Extends the base calculator service with async task management.
    """

    @staticmethod
    async def power_async(base: int, exponent: int) -> Tuple[int, float]:
        """Async wrapper for power calculation."""
        # For CPU-bound operations, run in executor
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: asyncio.run(CalculatorService.power(base, exponent))
        )

    @staticmethod
    async def fibonacci_async(n: int) -> Tuple[int, float]:
        """Async wrapper for Fibonacci calculation."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: asyncio.run(CalculatorService.fibonacci(n))
        )

    @staticmethod
    async def factorial_async(n: int) -> Tuple[int, float]:
        """Async wrapper for factorial calculation."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: asyncio.run(CalculatorService.factorial(n))
        )