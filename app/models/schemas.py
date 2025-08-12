"""Pydantic models for request/response validation."""
from datetime import datetime
from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel, Field, validator


class OperationType(str, Enum):
    """Enumeration of supported mathematical operations."""
    POWER = "power"
    FIBONACCI = "fibonacci"
    FACTORIAL = "factorial"


class MathOperationRequest(BaseModel):
    """Base request model for mathematical operations."""
    operation: OperationType
    value: int = Field(..., description="Input value for the operation")
    exponent: Optional[int] = Field(None, description="Exponent for power operation")

    @validator('value')
    def validate_value(cls, v, values):
        """Validate input value based on operation type."""
        if 'operation' in values:
            operation = values['operation']
            if operation == OperationType.FACTORIAL and v < 0:
                raise ValueError("Factorial requires non-negative integer")
            if operation == OperationType.FIBONACCI and v < 0:
                raise ValueError("Fibonacci requires non-negative integer")
        return v

    @validator('exponent')
    def validate_exponent(cls, v, values):
        """Validate exponent is provided for power operation."""
        if 'operation' in values and values['operation'] == OperationType.POWER:
            if v is None:
                raise ValueError("Exponent is required for power operation")
        return v

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "operation": "power",
                "value": 2,
                "exponent": 10
            }
        }


class MathOperationResponse(BaseModel):
    """Response model for mathematical operations."""
    operation: OperationType
    input_value: int
    exponent: Optional[int] = None
    result: Any
    cached: bool = Field(default=False, description="Whether result was from cache")
    computation_time_ms: float = Field(..., description="Computation time in milliseconds")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "operation": "power",
                "input_value": 2,
                "exponent": 10,
                "result": 1024,
                "cached": False,
                "computation_time_ms": 0.123,
                "timestamp": "2024-01-15T10:30:00"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthCheckResponse(BaseModel):
    """Health check response model."""
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"


class OperationHistoryItem(BaseModel):
    """Model for operation history."""
    id: int
    operation: str
    input_value: int
    exponent: Optional[int] = None
    result: Any
    computation_time_ms: float
    created_at: datetime
    ip_address: Optional[str] = None

    class Config:
        """Pydantic config."""
        from_attributes = True