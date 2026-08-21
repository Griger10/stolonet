from stolonet.domain.enums import MetricType
from stolonet.domain.interfaces.repositories import ReadingRepository
from stolonet.domain.models import MetricAverage


class CalculateAverageMetricValueImpl:
    def __init__(self, reading_repo: ReadingRepository) -> None:
        self._reading_repo = reading_repo

    async def __call__(
        self, node_id: str, metric_type: MetricType, hours: int = 24
    ) -> MetricAverage:
        return await self._reading_repo.calculate_telemetry_average_by_metric_type(
            node_id=node_id,
            metric_type=metric_type,
            hours=hours,
        )
