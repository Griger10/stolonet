from datetime import datetime

from pydantic import BaseModel


class Reading(BaseModel):
    metric: str
    value: float
    unit: str


class TelemetryEnvelope(BaseModel):
    node_id: str
    timestamp: datetime
    readings: list[Reading]
