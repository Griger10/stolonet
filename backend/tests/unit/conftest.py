from typing import cast

import pytest

from stolonet.application.usecases import SaveTelemetryDataImpl
from stolonet.application.usecases.read_telemetry_data import \
    ReadTelemetryDataImpl
from stolonet.domain.interfaces.repositories import ReadingRepository
from stolonet.domain.interfaces.usecases import (ReadTelemetryData,
                                                 SaveTelemetryData)


@pytest.fixture
def reading_repository(mocker) -> ReadingRepository:
    return cast(ReadingRepository, mocker.AsyncMock(spec=ReadingRepository))


@pytest.fixture
def read_telemetry_data(reading_repository) -> ReadTelemetryData:
    return ReadTelemetryDataImpl(reading_repository)


@pytest.fixture
def save_telemetry_data(reading_repository) -> SaveTelemetryData:
    return SaveTelemetryDataImpl(reading_repository)
