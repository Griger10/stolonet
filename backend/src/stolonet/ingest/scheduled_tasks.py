from dishka_faststream import FromDishka

from stolonet.domain.interfaces.usecases import MoveOldDataToArchiveUsecase
from stolonet.ingest.registry import register_scheduled_task

MOVE_OLD_DATA_TO_ARCHIVE_TOPIC = "stolonet/scheduled/move-old-data-to-archive"


@register_scheduled_task(
    topic=MOVE_OLD_DATA_TO_ARCHIVE_TOPIC,
    schedule=[{"cron": "0 3 * * *"}],
)
async def move_old_data_to_archive(usecase: FromDishka[MoveOldDataToArchiveUsecase]) -> None:
    await usecase()
