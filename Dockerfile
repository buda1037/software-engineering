FROM ghcr.io/astral-sh/uv:0.12.23-python3.15-rc-trixie-slim

ENV UV_PROJECT_ENVIRONMENT=/opt/app/.venv

WORKDIR /opt/app
COPY LICENSE README.md pyproject.toml uv.lock ./
COPY src ./src
RUN uv sync --frozen --no-default-groups --no-editable

ENTRYPOINT [".venv/bin/python", "-m", "hello_world"]
