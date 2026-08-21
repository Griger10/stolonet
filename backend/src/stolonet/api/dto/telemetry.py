from datetime import datetime

from pydantic import BaseModel

from stolonet.domain.enums import MetricType


class TimestampedReadingResponse(BaseModel):
    node_id: str
    metric: MetricType
    value: float
    unit: str
    timestamp: datetime


class MetricAverageResponse(BaseModel):
    node_id: str
    metric: MetricType
    average_value: float | None
    unit: str
    hours: int
