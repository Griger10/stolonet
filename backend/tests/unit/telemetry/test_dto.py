from pydantic import ValidationError
import pytest

from stolonet.domain.enums import MetricType
from stolonet.domain.enums.metric_type import unit_for
from stolonet.domain.models import Reading, TelemetryEnvelope
from stolonet.ingest.dto import ReadingDTO, TelemetryEnvelopeDTO


def test_telemetry_envelope_dto_to_domain_model(faker):
    # Arrange
    node_id = faker.pystr()
    timestamp = faker.date_time()
    dto = TelemetryEnvelopeDTO(
        node_id=node_id,
        timestamp=timestamp,
        readings=[
            ReadingDTO(
                metric=MetricType.SOIL_MOISTURE,
                value=faker.pyint(min_value=0, max_value=100),
                unit=unit_for(MetricType.SOIL_MOISTURE),
            ),
            ReadingDTO(
                metric=MetricType.AIR_TEMPERATURE,
                value=faker.pyint(min_value=-10, max_value=40),
                unit=unit_for(MetricType.AIR_TEMPERATURE),
            ),
        ],
    )

    # Act
    result = dto.to_domain_model()

    # Assert
    assert result == TelemetryEnvelope(
        node_id=node_id,
        timestamp=timestamp,
        readings=[
            Reading(
                metric=reading.metric,
                value=reading.value,
                unit=reading.unit,
            )
            for reading in dto.readings
        ],
    )


def test_telemetry_envelope_dto_to_domain_model_returns_telemetry_envelope(faker):
    # Arrange
    dto = TelemetryEnvelopeDTO(
        node_id=faker.pystr(),
        timestamp=faker.date_time(),
        readings=[
            ReadingDTO(
                metric=MetricType.SOIL_MOISTURE,
                value=faker.pyint(min_value=0, max_value=100),
                unit=unit_for(MetricType.SOIL_MOISTURE),
            ),
        ],
    )

    # Act
    result = dto.to_domain_model()

    # Assert
    assert isinstance(result, TelemetryEnvelope)
    assert all(isinstance(reading, Reading) for reading in result.readings)


def test_telemetry_envelope_dto_to_domain_model_preserves_reading_order(faker):
    # Arrange
    metrics = list(MetricType)
    dto = TelemetryEnvelopeDTO(
        node_id=faker.pystr(),
        timestamp=faker.date_time(),
        readings=[
            ReadingDTO(
                metric=metric,
                value=faker.pyfloat(min_value=-10, max_value=100),
                unit=unit_for(metric),
            )
            for metric in metrics
        ],
    )

    # Act
    result = dto.to_domain_model()

    # Assert
    assert [reading.metric for reading in result.readings] == metrics


def test_telemetry_envelope_dto_to_domain_model_with_empty_readings(faker):
    # Arrange
    node_id = faker.pystr()
    timestamp = faker.date_time()
    dto = TelemetryEnvelopeDTO(node_id=node_id, timestamp=timestamp, readings=[])

    # Act
    result = dto.to_domain_model()

    # Assert
    assert result == TelemetryEnvelope(node_id=node_id, timestamp=timestamp, readings=[])


def test_reading_dto_rejects_invalid_metric_type(faker):
    # Arrange
    invalid_payload = {
        "metric": faker.pystr(),
        "value": faker.pyfloat(min_value=-10, max_value=100),
        "unit": faker.pystr(),
    }

    # Act & Assert
    with pytest.raises(ValidationError):
        ReadingDTO(**invalid_payload)
