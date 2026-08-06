from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class MetricType(StrEnum):
    SOIL_MOISTURE = "soil_moisture"
    AIR_TEMPERATURE = "air_temperature"


class Reading(BaseModel):
    metric: MetricType
    value: float
    unit: str


class TelemetryEnvelope(BaseModel):
    node_id: str
    timestamp: datetime
    readings: list[Reading]
