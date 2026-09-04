import pytest
from fastapi import status
from fastapi.testclient import TestClient

from stolonet.domain.enums import MetricType
from stolonet.domain.enums.metric_type import unit_for
from stolonet.domain.models import MetricAverage, TimestampedReading


def test_read_telemetry(client: TestClient, reading_repository, faker) -> None:
    # Arrange
    node_id = faker.pystr()
    metric_type = MetricType.SOIL_MOISTURE
    reading = TimestampedReading(
        node_id=node_id,
        metric=metric_type,
        value=42.0,
        unit="%",
        timestamp=faker.date_time(),
    )
    reading_repository.get_telemetry_data_by_hours_window.return_value = [reading]

    # Act
    response = client.get(f"/telemetry/{node_id}", params={"metric_type": metric_type.value})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "node_id": node_id,
            "metric": metric_type.value,
            "value": 42.0,
            "unit": "%",
            "timestamp": reading.timestamp.isoformat(),
        }
    ]
    reading_repository.get_telemetry_data_by_hours_window.assert_called_once_with(
        node_id=node_id, hours=24, metric_type=metric_type, limit=100
    )


def test_read_telemetry_returns_empty_list_when_no_data(
    client: TestClient, reading_repository, faker
) -> None:
    # Arrange
    node_id = faker.pystr()
    metric_type = faker.random_element(list(MetricType))
    reading_repository.get_telemetry_data_by_hours_window.return_value = []

    # Act
    response = client.get(f"/telemetry/{node_id}", params={"metric_type": metric_type.value})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_read_telemetry_preserves_repository_order(
    client: TestClient, reading_repository, faker
) -> None:
    # Arrange
    node_id = faker.pystr()
    metric_type = MetricType.AIR_TEMPERATURE
    readings = [
        TimestampedReading(
            node_id=node_id,
            metric=metric_type,
            value=float(i),
            unit=unit_for(metric_type),
            timestamp=faker.date_time(),
        )
        for i in range(3)
    ]
    reading_repository.get_telemetry_data_by_hours_window.return_value = readings

    # Act
    response = client.get(f"/telemetry/{node_id}", params={"metric_type": metric_type.value})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert [item["value"] for item in response.json()] == [0.0, 1.0, 2.0]


def test_read_telemetry_uses_default_hours_and_limit(
    client: TestClient, reading_repository, faker
) -> None:
    # Arrange
    node_id = faker.pystr()
    metric_type = faker.random_element(list(MetricType))
    reading_repository.get_telemetry_data_by_hours_window.return_value = []

    # Act
    response = client.get(f"/telemetry/{node_id}", params={"metric_type": metric_type.value})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    reading_repository.get_telemetry_data_by_hours_window.assert_called_once_with(
        node_id=node_id, hours=24, metric_type=metric_type, limit=100
    )


def test_read_telemetry_custom_hours_and_limit(
    client: TestClient, reading_repository, faker
) -> None:
    # Arrange
    node_id = faker.pystr()
    metric_type = faker.random_element(list(MetricType))
    hours = faker.pyint(min_value=1, max_value=48)
    limit = faker.pyint(min_value=1, max_value=500)
    reading_repository.get_telemetry_data_by_hours_window.return_value = []

    # Act
    response = client.get(
        f"/telemetry/{node_id}",
        params={"metric_type": metric_type.value, "hours": hours, "limit": limit},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    reading_repository.get_telemetry_data_by_hours_window.assert_called_once_with(
        node_id=node_id, hours=hours, metric_type=metric_type, limit=limit
    )


@pytest.mark.parametrize("hours", [0, -1])
def test_read_telemetry_rejects_non_positive_hours(
    client: TestClient, reading_repository, faker, hours: int
) -> None:
    # Arrange
    node_id = faker.pystr()
    metric_type = faker.random_element(list(MetricType))

    # Act
    response = client.get(
        f"/telemetry/{node_id}", params={"metric_type": metric_type.value, "hours": hours}
    )

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    reading_repository.get_telemetry_data_by_hours_window.assert_not_called()


@pytest.mark.parametrize("limit", [0, -1])
def test_read_telemetry_rejects_non_positive_limit(
    client: TestClient, reading_repository, faker, limit: int
) -> None:
    # Arrange
    node_id = faker.pystr()
    metric_type = faker.random_element(list(MetricType))

    # Act
    response = client.get(
        f"/telemetry/{node_id}", params={"metric_type": metric_type.value, "limit": limit}
    )

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    reading_repository.get_telemetry_data_by_hours_window.assert_not_called()


def test_read_telemetry_requires_metric_type(client: TestClient, reading_repository, faker) -> None:
    # Arrange
    node_id = faker.pystr()

    # Act
    response = client.get(f"/telemetry/{node_id}")

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    reading_repository.get_telemetry_data_by_hours_window.assert_not_called()


def test_read_telemetry_rejects_unknown_metric_type(
    client: TestClient, reading_repository, faker
) -> None:
    # Arrange
    node_id = faker.pystr()

    # Act
    response = client.get(f"/telemetry/{node_id}", params={"metric_type": "unknown_metric"})

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    reading_repository.get_telemetry_data_by_hours_window.assert_not_called()


@pytest.mark.parametrize("metric_type", list(MetricType))
def test_read_telemetry_supports_all_metric_types(
    client: TestClient, reading_repository, faker, metric_type: MetricType
) -> None:
    # Arrange
    node_id = faker.pystr()
    reading = TimestampedReading(
        node_id=node_id,
        metric=metric_type,
        value=faker.pyfloat(min_value=-10, max_value=100),
        unit=unit_for(metric_type),
        timestamp=faker.date_time(),
    )
    reading_repository.get_telemetry_data_by_hours_window.return_value = [reading]

    # Act
    response = client.get(f"/telemetry/{node_id}", params={"metric_type": metric_type.value})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    body = response.json()[0]
    assert body["metric"] == metric_type.value
    assert body["unit"] == unit_for(metric_type)


def test_calculate_average(client: TestClient, reading_repository, faker) -> None:
    # Arrange
    node_id = faker.pystr()
    metric_type = MetricType.SOIL_MOISTURE
    hours = faker.pyint(min_value=1, max_value=24)
    value = faker.pyfloat(min_value=-10, max_value=100)
    average = MetricAverage(
        node_id=node_id,
        metric_type=metric_type,
        average_value=value,
        unit=unit_for(metric_type),
        hours=hours,
    )
    reading_repository.calculate_telemetry_average_by_metric_type.return_value = average

    # Act
    response = client.get(
        f"/telemetry/{node_id}/average", params={"metric_type": metric_type.value, "hours": hours}
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "node_id": node_id,
        "metric": metric_type.value,
        "average_value": value,
        "unit": unit_for(metric_type),
        "hours": hours,
    }
    reading_repository.calculate_telemetry_average_by_metric_type.assert_called_once_with(
        node_id=node_id, hours=hours, metric_type=metric_type
    )


def test_calculate_average_uses_default_hours(
    client: TestClient, reading_repository, faker
) -> None:
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
    response = client.get(
        f"/telemetry/{node_id}/average", params={"metric_type": metric_type.value}
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["hours"] == 24
    reading_repository.calculate_telemetry_average_by_metric_type.assert_called_once_with(
        node_id=node_id, hours=24, metric_type=metric_type
    )


def test_calculate_average_returns_null_when_no_data(
    client: TestClient, reading_repository, faker
) -> None:
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
    response = client.get(
        f"/telemetry/{node_id}/average", params={"metric_type": metric_type.value, "hours": hours}
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["average_value"] is None


@pytest.mark.parametrize("hours", [0, -1])
def test_calculate_average_rejects_non_positive_hours(
    client: TestClient, reading_repository, faker, hours: int
) -> None:
    # Arrange
    node_id = faker.pystr()
    metric_type = faker.random_element(list(MetricType))

    # Act
    response = client.get(
        f"/telemetry/{node_id}/average", params={"metric_type": metric_type.value, "hours": hours}
    )

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    reading_repository.calculate_telemetry_average_by_metric_type.assert_not_called()


def test_calculate_average_requires_metric_type(
    client: TestClient, reading_repository, faker
) -> None:
    # Arrange
    node_id = faker.pystr()

    # Act
    response = client.get(f"/telemetry/{node_id}/average")

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    reading_repository.calculate_telemetry_average_by_metric_type.assert_not_called()


def test_calculate_average_rejects_unknown_metric_type(
    client: TestClient, reading_repository, faker
) -> None:
    # Arrange
    node_id = faker.pystr()

    # Act
    response = client.get(f"/telemetry/{node_id}/average", params={"metric_type": "unknown_metric"})

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    reading_repository.calculate_telemetry_average_by_metric_type.assert_not_called()


@pytest.mark.parametrize("metric_type", list(MetricType))
def test_calculate_average_supports_all_metric_types(
    client: TestClient, reading_repository, faker, metric_type: MetricType
) -> None:
    # Arrange
    node_id = faker.pystr()
    average = MetricAverage(
        node_id=node_id,
        metric_type=metric_type,
        average_value=faker.pyfloat(min_value=-10, max_value=100),
        unit=unit_for(metric_type),
        hours=24,
    )
    reading_repository.calculate_telemetry_average_by_metric_type.return_value = average

    # Act
    response = client.get(
        f"/telemetry/{node_id}/average", params={"metric_type": metric_type.value}
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["metric"] == metric_type.value
    assert body["unit"] == unit_for(metric_type)
