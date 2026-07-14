from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

import stolonet.ingest.subscriber as subscribers_pkg

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
        broker.subscriber(topic=topic)(func)


def load_ingest_handlers() -> None:
    prefix = subscribers_pkg.__name__ + "."

    for module_info in pkgutil.walk_packages(
        subscribers_pkg.__path__,
        prefix,
    ):
        importlib.import_module(module_info.name)
