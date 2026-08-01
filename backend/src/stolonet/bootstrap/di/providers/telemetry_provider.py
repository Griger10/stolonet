from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from stolonet.application.usecases import SaveTelemetryDataImpl
from stolonet.domain.interfaces.repositories import ReadingRepository
from stolonet.domain.interfaces.usecases import SaveTelemetryData
from stolonet.infrastructure.persistence.repositories.reading_repository import \
    ReadingRepositoryImpl


class TelemetryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_repository(self, session: AsyncSession) -> ReadingRepository:
        return ReadingRepositoryImpl(session)

    @provide
    async def get_save_data_use_case(self, repo: ReadingRepository) -> SaveTelemetryData:
        return SaveTelemetryDataImpl(repo)
