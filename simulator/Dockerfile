FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.11.28 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app/simulator

COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --frozen

FROM python:3.13-slim
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/app/simulator/.venv
ENV PATH="/app/simulator/.venv/bin:${PATH}"
WORKDIR /app
COPY --from=builder /app/simulator/.venv /app/simulator/.venv

COPY . ./simulator

CMD python -m simulator
