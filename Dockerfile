FROM debian:11-slim AS build
RUN apt-get update
RUN apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /venv 
RUN /venv/bin/pip install --upgrade pip setuptools wheel
RUN /venv/bin/pip install poetry

FROM build AS build-venv
COPY pyproject.toml poetry.lock /
RUN /venv/bin/poetry export --without-hashes --format requirements.txt --output /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

FROM build-venv AS prod
# COPY --from=build-venv /venv /venv
COPY . /app
WORKDIR /app
ENTRYPOINT ["/venv/bin/python3", "src/main.py"]
