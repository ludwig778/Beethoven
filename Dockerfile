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
	libdbus-1-3 \
	libegl1 \
        libffi-dev \
	libfontconfig1 \
	libglib2.0-0 \
	libgl1 \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
	libxkbcommon0 \
        make && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PATH=$PATH:/root/.local/bin/

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install

COPY . .

ENTRYPOINT ["make"]
