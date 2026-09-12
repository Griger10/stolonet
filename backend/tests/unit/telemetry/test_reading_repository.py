from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy.dialects import postgresql


async def test_move_batch_old_telemetry_data_returns_rowcount(
    reading_repository_impl, db_session, faker
):
    # Arrange
    moved = faker.pyint(min_value=0, max_value=5000)
    db_session.execute.return_value.rowcount = moved

    # Act
    result = await reading_repository_impl.move_batch_old_telemetry_data(days=30, batch_size=2000)

    # Assert
    assert result == moved
    db_session.execute.assert_awaited_once()


async def test_move_batch_old_telemetry_data_moves_from_readings_into_archive(
    reading_repository_impl, db_session
):
    # Arrange
    db_session.execute.return_value.rowcount = 0

    # Act
    await reading_repository_impl.move_batch_old_telemetry_data(days=30, batch_size=2000)

    # Assert
    stmt = db_session.execute.call_args.args[0]
    compiled_sql = str(stmt.compile(dialect=postgresql.dialect()))

    assert "DELETE FROM readings" in compiled_sql
    assert "INSERT INTO readings_archive" in compiled_sql


async def test_move_batch_old_telemetry_data_filters_rows_older_than_cutoff(
    reading_repository_impl, db_session
):
    # Arrange
    db_session.execute.return_value.rowcount = 0

    # Act
    await reading_repository_impl.move_batch_old_telemetry_data(days=30, batch_size=2000)

    # Assert: comparison must select rows OLDER than the cutoff (<=), not newer (>=) -
    # a regression test for a past bug where the operator was flipped.
    stmt = db_session.execute.call_args.args[0]
    compiled = stmt.compile(dialect=postgresql.dialect())
    compiled_sql = str(compiled)

    assert "readings.created_at <=" in compiled_sql
    assert "readings.created_at >=" not in compiled_sql


async def test_move_batch_old_telemetry_data_uses_days_to_compute_cutoff(
    reading_repository_impl, db_session
):
    # Arrange
    db_session.execute.return_value.rowcount = 0
    days = 30

    # Act
    before_call = datetime.now(UTC)
    await reading_repository_impl.move_batch_old_telemetry_data(days=days, batch_size=2000)
    after_call = datetime.now(UTC)

    # Assert
    stmt = db_session.execute.call_args.args[0]
    compiled = stmt.compile(dialect=postgresql.dialect())
    cutoff = compiled.params["created_at_1"]

    assert before_call - timedelta(days=days) <= cutoff <= after_call - timedelta(days=days)


async def test_move_batch_old_telemetry_data_limits_selection_to_batch_size(
    reading_repository_impl, db_session, faker
):
    # Arrange
    db_session.execute.return_value.rowcount = 0
    batch_size = faker.pyint(min_value=1, max_value=5000)

    # Act
    await reading_repository_impl.move_batch_old_telemetry_data(days=30, batch_size=batch_size)

    # Assert
    stmt = db_session.execute.call_args.args[0]
    compiled = stmt.compile(dialect=postgresql.dialect())
    compiled_sql = str(compiled)

    assert "LIMIT" in compiled_sql
    assert batch_size in compiled.params.values()


async def test_move_batch_old_telemetry_data_propagates_session_exception(
    reading_repository_impl, db_session
):
    # Arrange
    db_session.execute.side_effect = ConnectionError("db unavailable")

    # Act & Assert
    with pytest.raises(ConnectionError):
        await reading_repository_impl.move_batch_old_telemetry_data(days=30, batch_size=2000)
