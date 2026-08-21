from stolonet.domain.enums import MetricType
from stolonet.domain.interfaces.repositories import ReadingRepository
from stolonet.domain.models import TimestampedReading


class ReadTelemetryDataImpl:
    def __init__(self, reading_repo: ReadingRepository) -> None:
        self._reading_repo = reading_repo

    async def __call__(
        self,
        node_id: str,
        metric_type: MetricType,
        hours: int = 24,
        limit: int = 100,
    ) -> list[TimestampedReading]:
        return await self._reading_repo.get_telemetry_data_by_hours_window(
            node_id=node_id,
            hours=hours,
            metric_type=metric_type,
            limit=limit,
        )
