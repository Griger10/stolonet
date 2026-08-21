from typing import cast

import pytest

from stolonet.application.transaction_manager import TransactionManager
from stolonet.application.usecases import CalculateAverageMetricValueImpl, SaveTelemetryDataImpl
from stolonet.application.usecases.read_telemetry_data import ReadTelemetryDataImpl
from stolonet.domain.interfaces.repositories import ReadingRepository
from stolonet.domain.interfaces.usecases import (
    CalculateAverageMetricValue,
    ReadTelemetryData,
    SaveTelemetryData,
)


@pytest.fixture
def reading_repository(mocker) -> ReadingRepository:
    return cast(ReadingRepository, mocker.AsyncMock(spec=ReadingRepository))


@pytest.fixture
def tx_manager(mocker) -> TransactionManager:
    return cast(TransactionManager, mocker.AsyncMock(spec=TransactionManager))


@pytest.fixture
def read_telemetry_data(reading_repository) -> ReadTelemetryData:
    return ReadTelemetryDataImpl(reading_repository)


@pytest.fixture
def save_telemetry_data(reading_repository, tx_manager) -> SaveTelemetryData:
    return SaveTelemetryDataImpl(reading_repository, tx_manager)


@pytest.fixture
def calculate_average_metric_value(reading_repository) -> CalculateAverageMetricValue:
    return CalculateAverageMetricValueImpl(reading_repository)
