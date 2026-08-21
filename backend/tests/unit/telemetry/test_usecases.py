import pytest

from stolonet.domain.enums import MetricType
from stolonet.domain.enums.metric_type import unit_for
from stolonet.domain.models import MetricAverage, Reading, TelemetryEnvelope, TimestampedReading


@pytest.mark.asyncio
async def test_read_telemetry_data(reading_repository, read_telemetry_data, faker):
    # Arrange
    node_id = faker.pystr()
    metric_type = faker.random_element(list(MetricType))
    hours = faker.pyint(min_value=0, max_value=24)
    limit = faker.pyint(min_value=1, max_value=100)
    data = [
        TimestampedReading(
            node_id=node_id,
            timestamp=faker.date_time(),
            metric=MetricType.SOIL_MOISTURE,
            value=faker.pyint(min_value=0, max_value=100),
            unit=unit_for(MetricType.SOIL_MOISTURE),
        ),
        TimestampedReading(
            node_id=node_id,
            timestamp=faker.date_time(),
            metric=MetricType.AIR_TEMPERATURE,
            value=faker.pyint(min_value=-10, max_value=40),
            unit=unit_for(MetricType.AIR_TEMPERATURE),
        ),
    ]
    reading_repository.get_telemetry_data_by_hours_window.return_value = data

    # Act
    result = await read_telemetry_data(
        node_id=node_id, metric_type=metric_type, hours=hours, limit=limit
    )

    # Assert
    assert result == data
    reading_repository.get_telemetry_data_by_hours_window.assert_called_once_with(
        node_id=node_id, hours=hours, metric_type=metric_type, limit=limit
    )


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
                unit=unit_for(MetricType.SOIL_MOISTURE),
            ),
            Reading(
                metric=MetricType.AIR_TEMPERATURE,
                value=faker.pyint(min_value=-10, max_value=40),
                unit=unit_for(MetricType.AIR_TEMPERATURE),
            ),
        ],
    )

    # Act
    result = await save_telemetry_data(data)

    # Assert
    assert result is None
    reading_repository.save_telemetry_data.assert_called_once_with(data)


@pytest.mark.asyncio
async def test_read_telemetry_data_returns_empty_list(
    reading_repository, read_telemetry_data, faker
):
    # Arrange
    node_id = faker.pystr()
    metric_type = faker.random_element(list(MetricType))
    hours = faker.pyint(min_value=0, max_value=24)
    reading_repository.get_telemetry_data_by_hours_window.return_value = []

    # Act
    result = await read_telemetry_data(node_id=node_id, metric_type=metric_type, hours=hours)

    # Assert
    assert result == []
    reading_repository.get_telemetry_data_by_hours_window.assert_called_once_with(
        node_id=node_id, hours=hours, metric_type=metric_type, limit=100
    )


@pytest.mark.asyncio
async def test_read_telemetry_data_uses_default_hours(
    reading_repository, read_telemetry_data, faker
):
    # Arrange
    node_id = faker.pystr()
    metric_type = faker.random_element(list(MetricType))
    reading_repository.get_telemetry_data_by_hours_window.return_value = []

    # Act
    result = await read_telemetry_data(node_id=node_id, metric_type=metric_type)

    # Assert
    assert result == []
    reading_repository.get_telemetry_data_by_hours_window.assert_called_once_with(
        node_id=node_id, hours=24, metric_type=metric_type, limit=100
    )


@pytest.mark.asyncio
async def test_read_telemetry_data_hours_zero_boundary(
    reading_repository, read_telemetry_data, faker
):
    # Arrange
    node_id = faker.pystr()
    metric_type = faker.random_element(list(MetricType))
    reading_repository.get_telemetry_data_by_hours_window.return_value = []

    # Act
    result = await read_telemetry_data(node_id=node_id, metric_type=metric_type, hours=0)

    # Assert
    assert result == []
    reading_repository.get_telemetry_data_by_hours_window.assert_called_once_with(
        node_id=node_id, hours=0, metric_type=metric_type, limit=100
    )


@pytest.mark.asyncio
async def test_read_telemetry_data_custom_limit(reading_repository, read_telemetry_data, faker):
    # Arrange
    node_id = faker.pystr()
    metric_type = faker.random_element(list(MetricType))
    limit = faker.pyint(min_value=1, max_value=99)
    reading_repository.get_telemetry_data_by_hours_window.return_value = []

    # Act
    result = await read_telemetry_data(node_id=node_id, metric_type=metric_type, limit=limit)

    # Assert
    assert result == []
    reading_repository.get_telemetry_data_by_hours_window.assert_called_once_with(
        node_id=node_id, hours=24, metric_type=metric_type, limit=limit
    )


@pytest.mark.asyncio
async def test_read_telemetry_data_propagates_repository_exception(
    reading_repository, read_telemetry_data, faker
):
    # Arrange
    node_id = faker.pystr()
    metric_type = faker.random_element(list(MetricType))
    hours = faker.pyint(min_value=0, max_value=24)
    reading_repository.get_telemetry_data_by_hours_window.side_effect = ConnectionError(
        "db unavailable"
    )

    # Act & Assert
    with pytest.raises(ConnectionError):
        await read_telemetry_data(node_id=node_id, metric_type=metric_type, hours=hours)
    reading_repository.get_telemetry_data_by_hours_window.assert_called_once_with(
        node_id=node_id, hours=hours, metric_type=metric_type, limit=100
    )


@pytest.mark.asyncio
async def test_save_telemetry_data_with_empty_readings(
    reading_repository, save_telemetry_data, faker
):
    # Arrange
    node_id = faker.pystr()
    data = TelemetryEnvelope(node_id=node_id, timestamp=faker.date_time(), readings=[])

    # Act
    result = await save_telemetry_data(data)

    # Assert
    assert result is None
    reading_repository.save_telemetry_data.assert_called_once_with(data)


@pytest.mark.asyncio
async def test_save_telemetry_data_propagates_repository_exception(
    reading_repository, save_telemetry_data, faker
):
    # Arrange
    node_id = faker.pystr()
    data = TelemetryEnvelope(
        node_id=node_id,
        timestamp=faker.date_time(),
        readings=[
            Reading(
                metric=MetricType.SOIL_MOISTURE,
                value=faker.pyint(min_value=0, max_value=100),
                unit=unit_for(MetricType.SOIL_MOISTURE),
            ),
        ],
    )
    reading_repository.save_telemetry_data.side_effect = RuntimeError("write failed")

    # Act & Assert
    with pytest.raises(RuntimeError):
        await save_telemetry_data(data)
    reading_repository.save_telemetry_data.assert_called_once_with(data)


@pytest.mark.asyncio
async def test_calculate_average_metric_value(
    reading_repository, calculate_average_metric_value, faker
):
    # Arrange
    node_id = faker.pystr()
    metric_type = faker.random_element(list(MetricType))
    hours = faker.pyint(min_value=1, max_value=24)
    average = MetricAverage(
        node_id=node_id,
        metric_type=metric_type,
        average_value=faker.pyfloat(min_value=-10, max_value=100),
        unit=unit_for(metric_type),
        hours=hours,
    )
    reading_repository.calculate_telemetry_average_by_metric_type.return_value = average

    # Act
    result = await calculate_average_metric_value(
        node_id=node_id, metric_type=metric_type, hours=hours
    )

    # Assert
    assert result == average
    reading_repository.calculate_telemetry_average_by_metric_type.assert_called_once_with(
        node_id=node_id, metric_type=metric_type, hours=hours
    )


@pytest.mark.asyncio
async def test_calculate_average_metric_value_uses_default_hours(
    reading_repository, calculate_average_metric_value, faker
):
    # Arrange
    node_id = faker.pystr()
    metric_type = faker.random_element(list(MetricType))
    average = MetricAverage(
        node_id=node_id,
        metric_type=metric_type,
        average_value=faker.pyfloat(min_value=-10, max_value=100),
        unit=unit_for(metric_type),
        hours=24,
    )
    reading_repository.calculate_telemetry_average_by_metric_type.return_value = average

    # Act
    result = await calculate_average_metric_value(node_id=node_id, metric_type=metric_type)

    # Assert
    assert result == average
    reading_repository.calculate_telemetry_average_by_metric_type.assert_called_once_with(
        node_id=node_id, metric_type=metric_type, hours=24
    )


@pytest.mark.asyncio
async def test_calculate_average_metric_value_no_data(
    reading_repository, calculate_average_metric_value, faker
):
    # Arrange
    node_id = faker.pystr()
    metric_type = faker.random_element(list(MetricType))
    hours = faker.pyint(min_value=1, max_value=24)
    average = MetricAverage(
        node_id=node_id,
        metric_type=metric_type,
        average_value=None,
        unit=unit_for(metric_type),
        hours=hours,
    )
    reading_repository.calculate_telemetry_average_by_metric_type.return_value = average

    # Act
    result = await calculate_average_metric_value(
        node_id=node_id, metric_type=metric_type, hours=hours
    )

    # Assert
    assert result.average_value is None
    reading_repository.calculate_telemetry_average_by_metric_type.assert_called_once_with(
        node_id=node_id, metric_type=metric_type, hours=hours
    )


@pytest.mark.asyncio
async def test_calculate_average_metric_value_propagates_repository_exception(
    reading_repository, calculate_average_metric_value, faker
):
    # Arrange
    node_id = faker.pystr()
    metric_type = faker.random_element(list(MetricType))
    hours = faker.pyint(min_value=1, max_value=24)
    reading_repository.calculate_telemetry_average_by_metric_type.side_effect = ConnectionError(
        "db unavailable"
    )

    # Act & Assert
    with pytest.raises(ConnectionError):
        await calculate_average_metric_value(node_id=node_id, metric_type=metric_type, hours=hours)
    reading_repository.calculate_telemetry_average_by_metric_type.assert_called_once_with(
        node_id=node_id, metric_type=metric_type, hours=hours
    )
