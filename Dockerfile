FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /app

ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY uv.lock pyproject.toml /app/
RUN --mount=type=cache,id=s/cdd02d9d-ce3d-4a12-8f17-5ed30b62c514-/root/.cache/uv,target=/root/.cache/uv \
    uv sync --locked --no-install-project

ENV PATH="/app/.venv/bin:$PATH"

COPY . /app
RUN --mount=type=cache,id=s/cdd02d9d-ce3d-4a12-8f17-5ed30b62c514-/root/.cache/uv,target=/root/.cache/uv \
    uv sync --locked

ENTRYPOINT []

CMD ["uv", "run", "main.py"]
