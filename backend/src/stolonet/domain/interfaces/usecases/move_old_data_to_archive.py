from typing import Protocol


class MoveOldDataToArchiveUsecase(Protocol):
    async def __call__(self) -> None: ...
