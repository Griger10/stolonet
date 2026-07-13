[group("lint")]
@backend_format:
    cd backend && uv run ruff format
    cd backend && uv run ruff check --fix
    cd backend && uv run isort .
    cd backend && uv run mypy --no-incremental
