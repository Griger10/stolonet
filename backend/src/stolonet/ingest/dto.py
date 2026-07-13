from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class MetricType(StrEnum):
    SOIL_MOISTURE = "soil_moisture"
    AIR_TEMPERATURE = "air_temp"


class Reading(BaseModel):
    metric: MetricType
    value: float
    unit: str


class TelemetryEnvelopeDTO(BaseModel):
    node_id: str
    timestamp: datetime
    readings: list[Reading]
