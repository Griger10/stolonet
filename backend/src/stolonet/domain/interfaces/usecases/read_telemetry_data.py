from typing import Protocol

from stolonet.domain.models import TimestampedReading


class ReadTelemetryData(Protocol):
    async def __call__(self, node_id: str, hours: int = 24) -> list[TimestampedReading]: ...
