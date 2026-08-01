from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.params import Query
from typing import Annotated

from stolonet.api.dto.telemetry import TimestampedReadingResponse
from stolonet.domain.interfaces.usecases import ReadTelemetryData

telemetry_router = APIRouter(route_class=DishkaRoute, prefix="/telemetry")


@telemetry_router.get("/{node_id}")
async def read_telemetry_endpoint(node_id: str, usecase: FromDishka[ReadTelemetryData], hours: Annotated[int, Query(gt=0)] = 24):
    domain_objects = await usecase(node_id, hours)
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
