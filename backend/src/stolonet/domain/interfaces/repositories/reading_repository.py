from typing import Protocol

from stolonet.domain.models import TelemetryEnvelope, TimestampedReading


class ReadingRepository(Protocol):
    async def save_telemetry_data(self, telemetry_data: TelemetryEnvelope) -> None: ...

    async def get_telemetry_data_by_hours_window(self, node_id: str, hours: int = 24) -> list[TimestampedReading]:
        ...
