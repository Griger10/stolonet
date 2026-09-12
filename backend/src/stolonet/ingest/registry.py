from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from dishka_faststream import inject
from zmqtt import QoS

if TYPE_CHECKING:
    from faststream.mqtt.fastapi import MQTTRouter
    from taskiq_faststream import BrokerWrapper
    from taskiq_faststream.types import ScheduledTask

type Handler = Callable[..., Awaitable[Any]]

SUBSCRIBERS_REGISTRY: dict[str, Handler] = {}


SCHEDULED_TASKS_REGISTRY: dict[str, list[ScheduledTask]] = {}


def register_subscriber(topic: str) -> Callable[[Handler], Handler]:
    def decorator(func: Handler) -> Handler:
        SUBSCRIBERS_REGISTRY[topic] = func
        return func

    return decorator


def register_scheduled_task(
    topic: str, schedule: list[ScheduledTask]
) -> Callable[[Handler], Handler]:
    def decorator(func: Handler) -> Handler:
        SCHEDULED_TASKS_REGISTRY[topic] = schedule
        return register_subscriber(topic)(func)

    return decorator


def register_all(broker: MQTTRouter) -> None:
    for topic, func in SUBSCRIBERS_REGISTRY.items():
        broker.subscriber(topic=topic, qos=QoS.AT_LEAST_ONCE)(inject(func))


def register_scheduled_tasks(taskiq_broker: BrokerWrapper) -> None:
    for topic, schedule in SCHEDULED_TASKS_REGISTRY.items():
        taskiq_broker.task(schedule=schedule, topic=topic)


def load_ingest_handlers() -> None:
    import stolonet.ingest

    prefix = stolonet.ingest.__name__ + "."

    for module_info in pkgutil.walk_packages(
        stolonet.ingest.__path__,
        prefix,
    ):
        importlib.import_module(module_info.name)
