FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /app

ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1

RUN --mount=type=cache,id=uv-cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

COPY . /app

CMD ["uv", "run", "main.py"]
