from stolonet.application.transaction_manager import TransactionManager
from stolonet.domain.interfaces.repositories import ReadingRepository

OLD_DATA_DAYS = 30
BATCH_SIZE = 2000


class MoveOldDataToArchiveUsecaseImpl:
    def __init__(self, repository: ReadingRepository, tx_manager: TransactionManager) -> None:
        self._reading_repo = repository
        self._tx_manager = tx_manager

    async def __call__(self) -> None:
        while True:
            moved = await self._reading_repo.move_batch_old_telemetry_data(
                OLD_DATA_DAYS, BATCH_SIZE
            )
            await self._tx_manager.commit()
            if moved < BATCH_SIZE:
                break
