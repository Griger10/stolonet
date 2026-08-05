import pytest

from stolonet.domain.enums import MetricType
from stolonet.domain.models import TimestampedReading, TelemetryEnvelope, Reading
from tests.unit.conftest import reading_repository


@pytest.mark.asyncio
async def test_read_telemetry_data(reading_repository, read_telemetry_data, faker):
    # Arrange
    node_id = faker.pystr()
    hours = faker.pyint(min_value=0, max_value=24)
    data = [
        TimestampedReading(
            node_id=node_id,
            timestamp=faker.date_time(),
            metric=MetricType.SOIL_MOISTURE,
            value=faker.pyint(min_value=0, max_value=100),
            unit="%"
        ),
        TimestampedReading(
            node_id=node_id,
            timestamp=faker.date_time(),
            metric=MetricType.AIR_TEMPERATURE,
            value=faker.pyint(min_value=-10, max_value=40),
            unit="C"
        ),
    ]
    reading_repository.get_telemetry_data_by_hours_window.return_value = data

    # Act
    result = await read_telemetry_data(node_id=node_id, hours=hours)

    # Assert
    assert result == data
    reading_repository.get_telemetry_data_by_hours_window.assert_called_once_with(node_id=node_id, hours=hours)


@pytest.mark.asyncio
async def test_save_telemetry_data(reading_repository, save_telemetry_data, faker):
    # Arrange
    node_id = faker.pystr()
    data = TelemetryEnvelope(
        node_id=node_id,
        timestamp=faker.date_time(),
        readings=[
            Reading(
                metric=MetricType.SOIL_MOISTURE,
                value=faker.pyint(min_value=0, max_value=100),
                unit="%"
            ),
            Reading(
                metric=MetricType.AIR_TEMPERATURE,
                value=faker.pyint(min_value=-10, max_value=40),
                unit="C"
            ),
        ])

    # Act
    result = await save_telemetry_data(data)

    # Assert
    assert result is None
    reading_repository.save_telemetry_data.assert_called_once_with(data)


@pytest.mark.asyncio
async def test_read_telemetry_data_returns_empty_list(reading_repository, read_telemetry_data, faker):
    # Arrange
    node_id = faker.pystr()
    hours = faker.pyint(min_value=0, max_value=24)
    reading_repository.get_telemetry_data_by_hours_window.return_value = []

    # Act
    result = await read_telemetry_data(node_id=node_id, hours=hours)

    # Assert
    assert result == []
    reading_repository.get_telemetry_data_by_hours_window.assert_called_once_with(node_id=node_id, hours=hours)


@pytest.mark.asyncio
async def test_read_telemetry_data_uses_default_hours(reading_repository, read_telemetry_data, faker):
    # Arrange
    node_id = faker.pystr()
    reading_repository.get_telemetry_data_by_hours_window.return_value = []

    # Act
    result = await read_telemetry_data(node_id=node_id)

    # Assert
    assert result == []
    reading_repository.get_telemetry_data_by_hours_window.assert_called_once_with(node_id=node_id, hours=24)


@pytest.mark.asyncio
async def test_read_telemetry_data_hours_zero_boundary(reading_repository, read_telemetry_data, faker):
    # Arrange
    node_id = faker.pystr()
    reading_repository.get_telemetry_data_by_hours_window.return_value = []

    # Act
    result = await read_telemetry_data(node_id=node_id, hours=0)

    # Assert
    assert result == []
    reading_repository.get_telemetry_data_by_hours_window.assert_called_once_with(node_id=node_id, hours=0)


@pytest.mark.asyncio
async def test_read_telemetry_data_propagates_repository_exception(reading_repository, read_telemetry_data, faker):
    # Arrange
    node_id = faker.pystr()
    hours = faker.pyint(min_value=0, max_value=24)
    reading_repository.get_telemetry_data_by_hours_window.side_effect = ConnectionError("db unavailable")

    # Act & Assert
    with pytest.raises(ConnectionError):
        await read_telemetry_data(node_id=node_id, hours=hours)
    reading_repository.get_telemetry_data_by_hours_window.assert_called_once_with(node_id=node_id, hours=hours)


@pytest.mark.asyncio
async def test_save_telemetry_data_with_empty_readings(reading_repository, save_telemetry_data, faker):
    # Arrange
    node_id = faker.pystr()
    data = TelemetryEnvelope(
        node_id=node_id,
        timestamp=faker.date_time(),
        readings=[]
    )

    # Act
    result = await save_telemetry_data(data)

    # Assert
    assert result is None
    reading_repository.save_telemetry_data.assert_called_once_with(data)


@pytest.mark.asyncio
async def test_save_telemetry_data_propagates_repository_exception(reading_repository, save_telemetry_data, faker):
    # Arrange
    node_id = faker.pystr()
    data = TelemetryEnvelope(
        node_id=node_id,
        timestamp=faker.date_time(),
        readings=[
            Reading(
                metric=MetricType.SOIL_MOISTURE,
                value=faker.pyint(min_value=0, max_value=100),
                unit="%"
            ),
        ])
    reading_repository.save_telemetry_data.side_effect = RuntimeError("write failed")

    # Act & Assert
    with pytest.raises(RuntimeError):
        await save_telemetry_data(data)
    reading_repository.save_telemetry_data.assert_called_once_with(data)
