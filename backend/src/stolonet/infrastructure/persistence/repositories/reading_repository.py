from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from stolonet.domain.enums import MetricType
from stolonet.domain.models import TelemetryEnvelope, TimestampedReading
from stolonet.infrastructure.persistence import ReadingORM


class ReadingRepositoryImpl:
    model: type[ReadingORM] = ReadingORM

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save_telemetry_data(self, data: TelemetryEnvelope) -> None:
        rows = [
            ReadingORM(
                time=data.timestamp,
                node_id=data.node_id,
                metric=r.metric,
                value=r.value,
                unit=r.unit,
            )
            for r in data.readings
        ]
        self._session.add_all(rows)
        await self._session.flush()

    async def get_telemetry_data_by_hours_window(
        self,
        node_id: str,
        metric_type: MetricType,
        hours: int = 24,
        limit: int = 100,
    ) -> list[TimestampedReading]:
        stmt = (
            select(self.model)
            .where(
                self.model.node_id == node_id,
                self.model.metric == metric_type,
                self.model.time >= datetime.now(UTC) - timedelta(hours=hours),
            )
            .limit(limit)
        )

        result = await self._session.execute(stmt)
        return [
            TimestampedReading(
                metric=MetricType(r.metric),
                value=r.value,
                unit=r.unit,
                timestamp=r.time,
                node_id=r.node_id,
            )
            for r in result.scalars().all()
        ]
