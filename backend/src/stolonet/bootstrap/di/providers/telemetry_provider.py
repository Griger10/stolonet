from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from stolonet.application.transaction_manager import TransactionManager
from stolonet.application.usecases import (
    SaveTelemetryDataImpl,
    CalculateAverageMetricValueImpl,
    ReadTelemetryDataImpl,
)
from stolonet.domain.interfaces.repositories import ReadingRepository
from stolonet.domain.interfaces.usecases import (
    ReadTelemetryData,
    SaveTelemetryData,
    CalculateAverageMetricValue,
)
from stolonet.infrastructure.persistence.repositories.reading_repository import (
    ReadingRepositoryImpl,
)


class TelemetryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_repository(self, session: AsyncSession) -> ReadingRepository:
        return ReadingRepositoryImpl(session)

    @provide
    async def get_save_data_use_case(
        self, repo: ReadingRepository, tx_manager: TransactionManager
    ) -> SaveTelemetryData:
        return SaveTelemetryDataImpl(repo, tx_manager)

    @provide
    async def get_read_data_use_case(self, repo: ReadingRepository) -> ReadTelemetryData:
        return ReadTelemetryDataImpl(repo)

    @provide
    async def get_calc_metric_average_use_case(
        self, repo: ReadingRepository
    ) -> CalculateAverageMetricValue:
        return CalculateAverageMetricValueImpl(repo)
