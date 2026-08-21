from typing import Protocol

from stolonet.domain.enums import MetricType
from stolonet.domain.models import TelemetryEnvelope, TimestampedReading, MetricAverage


class ReadingRepository(Protocol):
    async def save_telemetry_data(self, data: TelemetryEnvelope) -> None: ...

    async def get_telemetry_data_by_hours_window(
        self,
        node_id: str,
        metric_type: MetricType,
        hours: int = 24,
        limit: int = 100,
    ) -> list[TimestampedReading]: ...

    async def calculate_telemetry_average_by_metric_type(
        self,
        node_id: str,
        metric_type: MetricType,
        hours: int = 24,
    ) -> MetricAverage: ...
