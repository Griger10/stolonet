import asyncio

import uvicorn
from fastapi import FastAPI
from faststream.mqtt.fastapi import MQTTRouter

from stolonet.bootstrap.config import Config
from stolonet.ingest.registry import load_ingest_handlers, register_all

config = Config()
broker = MQTTRouter(
    host=config.mqtt_config.host,
    port=config.mqtt_config.port,
)

app = FastAPI(
    title="Stolonet",
    version="0.1.0",
    description="Stolonet backend",
    docs_url="/api/docs" if config.api_config.debug else None,
    redoc_url="/api/redoc" if config.api_config.debug else None,
)


async def run_api() -> None:
    load_ingest_handlers()
    register_all(broker)
    app.include_router(broker)
    server_config = uvicorn.Config(
        app=app, host=config.api_config.host, port=config.api_config.port
    )
    server = uvicorn.Server(server_config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run_api())
