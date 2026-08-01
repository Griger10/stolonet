from datetime import datetime

from pydantic import BaseModel

from stolonet.domain.enums import MetricType


class TimestampedReadingResponse(BaseModel):
    node_id: str
    metric: MetricType
    value: float
    unit: str
    timestamp: datetime
