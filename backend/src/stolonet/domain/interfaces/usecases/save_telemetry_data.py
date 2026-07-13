from typing import Protocol

from stolonet.domain.models import TelemetryEnvelope


class SaveTelemetryData(Protocol):
    async def __call__(self, telemetry_data: TelemetryEnvelope) -> None: ...
