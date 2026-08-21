from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.params import Query

from stolonet.api.dto.telemetry import TimestampedReadingResponse, MetricAverageResponse
from stolonet.domain.enums import MetricType
from stolonet.domain.enums.metric_type import unit_for
from stolonet.domain.interfaces.usecases import ReadTelemetryData, CalculateAverageMetricValue

telemetry_router = APIRouter(route_class=DishkaRoute, prefix="/telemetry", tags=["telemetry"])


@telemetry_router.get("/{node_id}")
async def read_telemetry_endpoint(
    node_id: str,
    usecase: FromDishka[ReadTelemetryData],
    metric_type: Annotated[MetricType, Query()],
    hours: Annotated[int, Query(gt=0)] = 24,
    limit: Annotated[int, Query(gt=0)] = 100,
) -> list[TimestampedReadingResponse]:
    domain_objects = await usecase(
        node_id=node_id, hours=hours, metric_type=metric_type, limit=limit
    )
    return [
        TimestampedReadingResponse(
            node_id=domain_object.node_id,
            timestamp=domain_object.timestamp,
            value=domain_object.value,
            metric=domain_object.metric,
            unit=domain_object.unit,
        )
        for domain_object in domain_objects
    ]


@telemetry_router.get("/{node_id}/average")
async def get_telemetry_average(
    node_id: str,
    usecase: FromDishka[CalculateAverageMetricValue],
    metric_type: Annotated[MetricType, Query()],
    hours: Annotated[int, Query(gt=0)] = 24,
) -> MetricAverageResponse:
    metric_average = await usecase(node_id=node_id, metric_type=metric_type, hours=hours)

    return MetricAverageResponse(
        node_id=node_id,
        metric=metric_type,
        hours=hours,
        average_value=metric_average.average_value,
        unit=unit_for(metric_type),
    )
