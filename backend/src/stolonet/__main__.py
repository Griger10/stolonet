import asyncio
import logging
from contextlib import suppress

import uvicorn
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka as setup_fastapi_dishka
from dishka_faststream import setup_dishka as setup_faststream_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from faststream.mqtt.fastapi import MQTTRouter
from taskiq.api import run_scheduler_task
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_faststream import BrokerWrapper, StreamScheduler

from stolonet.api.routers.telemetry import telemetry_router
from stolonet.bootstrap.config import Config
from stolonet.bootstrap.di.ioc import create_container
from stolonet.bootstrap.log import configure_logging
from stolonet.ingest.registry import load_ingest_handlers, register_all, register_scheduled_tasks

logger = logging.getLogger(__name__)


def create_app(
    config: Config,
    container: AsyncContainer,
    mqtt_router: MQTTRouter,
    taskiq_broker: BrokerWrapper,
) -> FastAPI:
    app = FastAPI(
        title="Stolonet",
        version="0.1.0",
        description="Stolonet backend",
        docs_url="/api/docs" if config.api_config.debug else None,
        redoc_url="/api/redoc" if config.api_config.debug else None,
        openapi_url="/api/openapi.json" if config.api_config.debug else None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_faststream_dishka(container=container, broker=mqtt_router.broker, auto_inject=True)
    setup_fastapi_dishka(container=container, app=app)

    load_ingest_handlers()
    register_all(mqtt_router)
    register_scheduled_tasks(taskiq_broker)
    app.include_router(mqtt_router)
    app.include_router(telemetry_router)

    return app


def _log_scheduler_failure(task: asyncio.Task[None]) -> None:
    if task.cancelled():
        return
    exc = task.exception()
    if exc is not None:
        logger.error("Scheduler task stopped unexpectedly", exc_info=exc)


async def run_api(config: Config, app: FastAPI) -> None:
    server_config = uvicorn.Config(
        app=app, host=config.api_config.host, port=config.api_config.port
    )
    server = uvicorn.Server(server_config)
    await server.serve()


async def main() -> None:
    config = Config()
    container = create_container()
    mqtt_router = MQTTRouter(
        host=config.mqtt_config.host,
        port=config.mqtt_config.port,
    )
    taskiq_broker = BrokerWrapper(mqtt_router.broker)
    scheduler = StreamScheduler(
        broker=taskiq_broker,
        sources=[LabelScheduleSource(taskiq_broker)],
    )

    app = create_app(config, container, mqtt_router, taskiq_broker)

    scheduler_task = asyncio.create_task(run_scheduler_task(scheduler))
    scheduler_task.add_done_callback(_log_scheduler_failure)
    try:
        await run_api(config, app)
    finally:
        scheduler_task.cancel()
        with suppress(asyncio.CancelledError):
            await scheduler_task


if __name__ == "__main__":
    configure_logging()
    asyncio.run(main())
