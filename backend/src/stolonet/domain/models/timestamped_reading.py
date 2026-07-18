from dataclasses import dataclass
from datetime import datetime

from stolonet.domain.enums.metric_type import MetricType


@dataclass(slots=True, frozen=True)
class TimestampedReading:
    node_id: str
    metric: MetricType
    value: float
    unit: str
    timestamp: datetime
