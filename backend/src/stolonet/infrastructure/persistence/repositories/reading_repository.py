from datetime import UTC, datetime, timedelta
from typing import Any, cast

from sqlalchemy import select, func, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from stolonet.domain.enums import MetricType
from stolonet.domain.enums.metric_type import unit_for
from stolonet.domain.models import TelemetryEnvelope, TimestampedReading, MetricAverage
from stolonet.infrastructure.persistence import ReadingORM
from stolonet.infrastructure.persistence.models.reading_archive import ReadingArchiveORM


class ReadingRepositoryImpl:
    model: type[ReadingORM] = ReadingORM
    archive_model: type[ReadingArchiveORM] = ReadingArchiveORM

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

    async def calculate_telemetry_average_by_metric_type(
        self,
        node_id: str,
        metric_type: MetricType,
        hours: int = 24,
    ) -> MetricAverage:
        stmt = select(func.avg(self.model.value)).where(
            self.model.node_id == node_id,
            self.model.metric == metric_type,
            self.model.time >= datetime.now(UTC) - timedelta(hours=hours),
        )

        result = await self._session.execute(stmt)
        value = result.scalar_one_or_none()

        return MetricAverage(
            node_id=node_id,
            average_value=value,
            metric_type=metric_type,
            unit=unit_for(metric_type),
            hours=hours,
        )

    async def move_batch_old_telemetry_data(self, days: int, batch_size: int) -> int:
        ids_subquery = (
            select(self.model.reading_id)
            .where(self.model.created_at <= datetime.now(UTC) - timedelta(days=days))
            .order_by(self.model.created_at)
            .limit(batch_size)
        )

        moved_cte = (
            delete(self.model)
            .where(self.model.reading_id.in_(ids_subquery))
            .returning(*self.model.__table__.columns)
            .cte("moved")
        )

        columns = [c.name for c in self.model.__table__.columns]

        stmt = insert(self.archive_model).from_select(columns, select(moved_cte))

        result = await self._session.execute(stmt)

        return cast(CursorResult[Any], result).rowcount
