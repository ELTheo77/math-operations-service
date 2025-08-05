"""API endpoints for mathematical operations."""
import json
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.models.schemas import (
    MathOperationRequest,
    MathOperationResponse,
    OperationType,
    HealthCheckResponse,
    OperationHistoryItem,
    ErrorResponse
)
from app.models.database import OperationHistory
from app.services.calculator import CalculatorService
from app.services.cache import cache_service
from app.db.session import get_db
from app.core.config import settings

router = APIRouter()
calculator = CalculatorService()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    return HealthCheckResponse(
        status="healthy",
        version=settings.VERSION
    )


@router.post("/calculate", response_model=MathOperationResponse)
async def calculate(
    request: MathOperationRequest,
    req: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Perform mathematical calculation.
    
    Supports:
    - Power: Calculate base^exponent
    - Fibonacci: Get n-th Fibonacci number
    - Factorial: Calculate n!
    """
    try:
        # Check cache first
        cached_result = await cache_service.get(
            request.operation.value,
            request.value,
            request.exponent
        )
        
        if cached_result is not None:
            # Return cached result
            result = cached_result
            computation_time = 0.0
            from_cache = True
        else:
            # Perform calculation
            if request.operation == OperationType.POWER:
                result, computation_time = await calculator.power(
                    request.value,
                    request.exponent
                )
            elif request.operation == OperationType.FIBONACCI:
                result, computation_time = await calculator.fibonacci(request.value)
            elif request.operation == OperationType.FACTORIAL:
                result, computation_time = await calculator.factorial(request.value)
            else:
                raise ValueError(f"Unsupported operation: {request.operation}")
            
            # Cache the result
            await cache_service.set(
                request.operation.value,
                request.value,
                result,
                request.exponent
            )
            from_cache = False
        
        # Store in database
        operation_record = OperationHistory(
            operation=request.operation.value,
            input_value=request.value,
            exponent=request.exponent,
            result=str(result),  # Store as string to handle large numbers
            computation_time_ms=computation_time,
            ip_address=req.client.host
        )
        db.add(operation_record)
        await db.commit()
        
        # Return response
        return MathOperationResponse(
            operation=request.operation,
            input_value=request.value,
            exponent=request.exponent,
            result=result,
            cached=from_cache,
            computation_time_ms=computation_time
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/history", response_model=List[OperationHistoryItem])
async def get_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    operation: Optional[OperationType] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get operation history with optional filtering."""
    query = select(OperationHistory)
    
    if operation:
        query = query.where(OperationHistory.operation == operation.value)
    
    query = query.order_by(desc(OperationHistory.created_at))
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    operations = result.scalars().all()
    
    # Convert to response model
    return [
        OperationHistoryItem(
            id=op.id,
            operation=op.operation,
            input_value=op.input_value,
            exponent=op.exponent,
            result=json.loads(op.result) if op.result.startswith('[') else int(op.result),
            computation_time_ms=op.computation_time_ms,
            created_at=op.created_at,
            ip_address=op.ip_address
        )
        for op in operations
    ]


@router.get("/cache/stats")
async def get_cache_stats():
    """Get cache statistics."""
    return await cache_service.get_stats()


@router.delete("/cache")
async def clear_cache():
    """Clear the cache."""
    await cache_service.clear()
    return {"message": "Cache cleared successfully"}