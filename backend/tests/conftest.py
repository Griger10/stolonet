from typing import cast

import pytest

from stolonet.application.transaction_manager import TransactionManager
from stolonet.domain.interfaces.repositories import ReadingRepository


@pytest.fixture
def reading_repository(mocker) -> ReadingRepository:
    return cast(ReadingRepository, mocker.AsyncMock(spec=ReadingRepository))


@pytest.fixture
def tx_manager(mocker) -> TransactionManager:
    return cast(TransactionManager, mocker.AsyncMock(spec=TransactionManager))
