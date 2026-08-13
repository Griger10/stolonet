from dishka import Provider

from stolonet.bootstrap.di.providers.database import DatabaseProvider
from stolonet.bootstrap.di.providers.telemetry_provider import TelemetryProvider


def get_providers() -> list[Provider]:
    return [
        DatabaseProvider(),
        TelemetryProvider(),
    ]
