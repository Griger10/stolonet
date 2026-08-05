from dishka_faststream import FromDishka

from stolonet.domain.interfaces.usecases import SaveTelemetryData
from stolonet.ingest.dto import TelemetryEnvelopeDTO
from stolonet.ingest.registry import register_subscriber


@register_subscriber("stolonet/telemetry/+")
async def handle_telemetry(
    message: TelemetryEnvelopeDTO, usecase: FromDishka[SaveTelemetryData]
) -> None:
    await usecase(message.to_domain_model())
