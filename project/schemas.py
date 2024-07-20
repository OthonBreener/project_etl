from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class DataSchema(BaseModel):
    timestamp: datetime
    wind_speed: float
    power: float
    ambient_temperature: float


class Options(BaseModel):
    timestamp: int = 1
    wind_speed: int = 1
    power: int = 1
    ambient_temperature: int = 1
    skip: int = (0,)
    limit: int = (10,)


class DataAggregationsSchema(BaseModel):
    timestamp: datetime
    mean: float
    min: float
    max: float
    std: float


class SignalSchema(BaseModel):
    name: str
    data: list[DataAggregationsSchema]


class SignalName(str, Enum):
    wind_speed = "wind_speed"
    power = "power"
