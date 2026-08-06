from stolonet.application.transaction_manager import TransactionManager
from stolonet.domain.interfaces.repositories import ReadingRepository
from stolonet.domain.models import TelemetryEnvelope


class SaveTelemetryDataImpl:
    def __init__(self, reading_repo: ReadingRepository, tx_manager: TransactionManager) -> None:
        self._reading_repo = reading_repo
        self._tx_manager = tx_manager

    async def __call__(self, telemetry_data: TelemetryEnvelope) -> None:
        await self._reading_repo.save_telemetry_data(telemetry_data)
        await self._tx_manager.commit()
