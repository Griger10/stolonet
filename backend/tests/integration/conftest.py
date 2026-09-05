from collections.abc import Iterable

import pytest
import pytest_asyncio
from dishka import Provider, Scope, provide, make_async_container
from faststream.mqtt.fastapi import MQTTRouter
from fastapi.testclient import TestClient

from stolonet.__main__ import create_app
from stolonet.application.transaction_manager import TransactionManager
from stolonet.application.usecases import (
    SaveTelemetryDataImpl,
    ReadTelemetryDataImpl,
    CalculateAverageMetricValueImpl,
)
from stolonet.domain.interfaces.repositories import ReadingRepository
from stolonet.domain.interfaces.usecases import (
    SaveTelemetryData,
    ReadTelemetryData,
    CalculateAverageMetricValue,
)


class TestDatabaseProvider(Provider):
    scope = Scope.APP

    def __init__(self, tx_manager: TransactionManager) -> None:
        self.tx_manager = tx_manager
        super().__init__()

    @provide(scope=Scope.REQUEST)
    async def get_transaction_manager(self) -> TransactionManager:
        return self.tx_manager


class TestTelemetryProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self, repo: ReadingRepository) -> None:
        self.repo = repo
        super().__init__()

    @provide
    async def get_repository(self) -> ReadingRepository:
        return self.repo

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


@pytest.fixture
def tx_manager(mocker):
    return mocker.AsyncMock(spec=TransactionManager)


@pytest.fixture
def reading_repository(mocker):
    return mocker.AsyncMock(spec=ReadingRepository)


@pytest_asyncio.fixture
async def container(tx_manager, reading_repository):
    container = make_async_container(
        TestDatabaseProvider(tx_manager),
        TestTelemetryProvider(reading_repository),
    )
    yield container
    await container.close()


@pytest_asyncio.fixture
async def request_container(container):
    async with container() as request_container:
        yield request_container


@pytest.fixture
def config(mocker):
    config = mocker.Mock()
    config.api_config.debug = False
    config.api_config.host = "0.0.0.0"
    config.api_config.port = 8000
    return config


@pytest.fixture
def mqtt_router(mocker) -> MQTTRouter:
    router = MQTTRouter(host="localhost", port=1883)
    mocker.patch.object(router.broker, "start", mocker.AsyncMock())
    mocker.patch.object(router.broker, "stop", mocker.AsyncMock())
    return router


@pytest.fixture
def client(container, config, mqtt_router) -> Iterable[TestClient]:
    app = create_app(
        container=container,
        config=config,
        mqtt_router=mqtt_router,
    )
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture
async def save_telemetry_usecase(request_container):
    return await request_container.get(SaveTelemetryData)


@pytest_asyncio.fixture
async def read_telemetry_usecase(request_container):
    return await request_container.get(ReadTelemetryData)


@pytest_asyncio.fixture
async def calc_metric_average_usecase(request_container):
    return await request_container.get(CalculateAverageMetricValue)
