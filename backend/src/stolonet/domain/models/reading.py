from dataclasses import dataclass

from stolonet.domain.enums.metric_type import MetricType


@dataclass(slots=True, frozen=True)
class Reading:
    metric: MetricType
    value: float
    unit: str
