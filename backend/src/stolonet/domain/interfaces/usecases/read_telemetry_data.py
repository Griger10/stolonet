from typing import Protocol

from stolonet.domain.enums import MetricType
from stolonet.domain.models import TimestampedReading


class ReadTelemetryData(Protocol):
    async def __call__(
        self,
        node_id: str,
        metric_type: MetricType,
        hours: int = 24,
        limit: int = 100,
    ) -> list[TimestampedReading]: ...
