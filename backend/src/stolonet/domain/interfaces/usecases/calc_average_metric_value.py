from typing import Protocol

from stolonet.domain.enums import MetricType
from stolonet.domain.models import MetricAverage


class CalculateAverageMetricValue(Protocol):
    async def __call__(
        self, node_id: str, metric_type: MetricType, hours: int = 24
    ) -> MetricAverage | None: ...
