FROM python:3.8-slim-buster

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && \
    apt install -y \
        build-essential \
        curl \
        gcc \
        git \
        inotify-tools \
        libasound-dev \
        libbz2-dev \
        libffi-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        make && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 - && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PATH=$PATH:/root/.poetry/bin/

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install

COPY . .

ENTRYPOINT ["make"]
