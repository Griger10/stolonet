[group("lint")]
@backend_format:
    cd backend && VIRTUAL_ENV= uv run ruff format
    cd backend && VIRTUAL_ENV= uv run ruff check --fix
    cd backend && VIRTUAL_ENV= uv run isort .
    cd backend && VIRTUAL_ENV= uv run mypy --no-incremental

[group("test")]
@backend_test:
    cd backend && VIRTUAL_ENV= uv run pytest tests/unit -v

[group("migrations")]
@backend_migrate:
    cd backend && VIRTUAL_ENV= uv run alembic upgrade head

[group("pre-commit")]
@pre-commit:
    cd backend && uv run pre-commit run --all-files
