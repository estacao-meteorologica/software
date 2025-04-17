from pydantic import BaseModel
from datetime import datetime

class Status(BaseModel):
    id: str
    timestamp: datetime = None
    temperature: float = None
    humidity: float = None
    pressure: float = None
    timestamp: datetime = None
    temperature: float = None
    humidity: float = None
    pressure: float = None
    co: float = None
    co2: float = None
    methane: float = None
