FROM ghcr.io/astral-sh/uv:0.12.23-python3.15-rc-trixie-slim

ENV UV_PROJECT_ENVIRONMENT=/opt/app/.venv UVICORN_HOST=0.0.0.0

WORKDIR /opt/app
COPY LICENSE README.md pyproject.toml uv.lock ./
COPY src ./src
RUN uv sync --frozen --no-default-groups --no-editable

EXPOSE 8000

ENTRYPOINT [".venv/bin/python", "-m", "student"]
