from enum import StrEnum


class MetricType(StrEnum):
    SOIL_MOISTURE = "soil_moisture"
    AIR_TEMPERATURE = "air_temperature"


METRIC_UNITS: dict[MetricType, str] = {
    MetricType.SOIL_MOISTURE: "%",
    MetricType.AIR_TEMPERATURE: "C",
}


def unit_for(metric_type: MetricType) -> str:
    return METRIC_UNITS[metric_type]
