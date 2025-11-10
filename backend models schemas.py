from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SensorData(BaseModel):
    timestamp: Optional[float] = None
    co2: float  # Must be >0
    temp: Optional[float] = None
    prediction: Optional[str] = None

    class Config:
        extra = "allow"  # Allow extra fields