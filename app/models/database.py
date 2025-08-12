"""SQLAlchemy database models."""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OperationHistory(Base):
    """Database model for storing operation history."""
    __tablename__ = "operation_history"

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String(50), nullable=False, index=True)
    input_value = Column(Integer, nullable=False)
    exponent = Column(Integer, nullable=True)
    result = Column(Text, nullable=False)  # Store as text to handle large numbers
    computation_time_ms = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_address = Column(String(45), nullable=True)  # Support IPv6

    def __repr__(self):
        """String representation."""
        return (
            f"<OperationHistory(id={self.id}, operation={self.operation}, "
            f"input_value={self.input_value}, result={self.result})>"
        )