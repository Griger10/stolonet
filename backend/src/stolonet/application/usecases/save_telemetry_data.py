from stolonet.domain.interfaces.repositories import ReadingRepository
from stolonet.domain.models import TelemetryEnvelope


class SaveTelemetryDataImpl:
    def __init__(self, reading_repo: ReadingRepository) -> None:
        self._reading_repo = reading_repo

    async def __call__(self, telemetry_data: TelemetryEnvelope) -> None:
        await self._reading_repo.save_telemetry_data(telemetry_data)
