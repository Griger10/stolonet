[group("lint")]
@backend_format:
    cd backend && uv run ruff format
    cd backend && uv run ruff check --fix
    cd backend && uv run isort .
    cd backend && uv run mypy --no-incremental

[group("test")]
@backend_test:
    cd backend && uv run pytest tests/unit -v

[group("migrations")]
@backend_migrate:
    cd backend && uv run alembic upgrade head
