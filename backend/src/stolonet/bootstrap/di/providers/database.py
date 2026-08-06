from collections.abc import AsyncGenerator
from typing import Any

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from stolonet.application.transaction_manager import TransactionManager
from stolonet.bootstrap.config import Config
from stolonet.infrastructure.persistence.transaction_manager import \
    ORMTransactionManager


class DatabaseProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_engine(self, config: Config) -> AsyncGenerator[AsyncEngine, Any]:
        engine = create_async_engine(url=config.database_config.database_url)
        yield engine
        await engine.dispose(close=True)

    @provide
    async def get_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, pool: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, Any]:
        async with pool() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_transaction_manager(self, session: AsyncSession) -> TransactionManager:
        return ORMTransactionManager(session)
