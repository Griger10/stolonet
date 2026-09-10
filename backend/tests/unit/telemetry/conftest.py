from collections.abc import Iterable

import pytest
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import FastapiProvider
from fastapi.testclient import TestClient
from faststream.mqtt.fastapi import MQTTRouter

from stolonet.__main__ import create_app
from stolonet.application.transaction_manager import TransactionManager
from stolonet.application.usecases import (
    CalculateAverageMetricValueImpl,
    ReadTelemetryDataImpl,
    SaveTelemetryDataImpl,
)
from stolonet.bootstrap.config import APIConfig, Config, DatabaseConfig, MQTTConfig
from stolonet.bootstrap.di.providers.database import DatabaseProvider
from stolonet.bootstrap.di.providers.telemetry_provider import TelemetryProvider
from stolonet.domain.interfaces.repositories import ReadingRepository
from stolonet.domain.interfaces.usecases import (
    CalculateAverageMetricValue,
    ReadTelemetryData,
    SaveTelemetryData,
)


@pytest.fixture
def read_telemetry_data(reading_repository) -> ReadTelemetryData:
    return ReadTelemetryDataImpl(reading_repository)


@pytest.fixture
def save_telemetry_data(reading_repository, tx_manager) -> SaveTelemetryData:
    return SaveTelemetryDataImpl(reading_repository, tx_manager)


@pytest.fixture
def calculate_average_metric_value(reading_repository) -> CalculateAverageMetricValue:
    return CalculateAverageMetricValueImpl(reading_repository)


class MockInfraProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self, repo: ReadingRepository, tx_manager: TransactionManager) -> None:
        super().__init__()
        self._repo = repo
        self._tx_manager = tx_manager

    @provide(override=True)
    async def get_repository(self) -> ReadingRepository:
        return self._repo

    @provide(override=True)
    async def get_transaction_manager(self) -> TransactionManager:
        return self._tx_manager


@pytest.fixture
def test_config() -> Config:
    return Config(
        mqtt_config=MQTTConfig(host="localhost", port=1883),
        database_config=DatabaseConfig(
            host="localhost",
            port=5432,
            user="test",
            password="test",
            db="test",
        ),
        api_config=APIConfig(host="0.0.0.0", port=8000, debug=False),
    )


@pytest.fixture
async def container(test_config, reading_repository, tx_manager):
    container = make_async_container(
        DatabaseProvider(),
        TelemetryProvider(),
        FastapiProvider(),
        MockInfraProvider(reading_repository, tx_manager),
        context={Config: test_config},
    )
    yield container
    await container.close()


@pytest.fixture
def mqtt_router(mocker) -> MQTTRouter:
    router = MQTTRouter(host="localhost", port=1883)
    mocker.patch.object(router.broker, "start", mocker.AsyncMock())
    mocker.patch.object(router.broker, "stop", mocker.AsyncMock())
    return router


@pytest.fixture
def client(container, test_config, mqtt_router) -> Iterable[TestClient]:
    app = create_app(config=test_config, container=container, mqtt_router=mqtt_router)
    with TestClient(app) as client:
        yield client
