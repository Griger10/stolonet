from dataclasses import dataclass

from stolonet.domain.enums import MetricType


@dataclass(frozen=True, slots=True)
class MetricAverage:
    node_id: str
    metric_type: MetricType
    average_value: float
    unit: str
    period_hours: int
