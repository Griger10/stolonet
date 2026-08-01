from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from stolonet.bootstrap.config import Config
from stolonet.bootstrap.di.providers import get_providers


def create_container() -> AsyncContainer:
    context = {
        Config: Config(),
    }

    return make_async_container(
        *get_providers(),
        FastapiProvider(),
        context=context,
    )
