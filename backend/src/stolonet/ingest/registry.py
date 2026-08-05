from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from dishka_faststream import inject

if TYPE_CHECKING:
    from faststream.mqtt.fastapi import MQTTRouter

type Handler = Callable[..., Awaitable[Any]]

SUBSCRIBERS_REGISTRY: dict[str, Handler] = {}


def register_subscriber(topic: str) -> Callable[[Handler], Handler]:
    def decorator(func: Handler) -> Handler:
        SUBSCRIBERS_REGISTRY[topic] = func
        return func

    return decorator


def register_all(broker: MQTTRouter) -> None:
    for topic, func in SUBSCRIBERS_REGISTRY.items():
        broker.subscriber(topic=topic)(inject(func))


def load_ingest_handlers() -> None:
    import stolonet.ingest

    prefix = stolonet.ingest.__name__ + "."

    for module_info in pkgutil.walk_packages(
            stolonet.ingest.__path__,
            prefix,
    ):
        importlib.import_module(module_info.name)
