FROM ubuntu:focal

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
        make \
        python3 \
        python3-pip && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 - && \
    curl -sSL https://pyenv.run | bash && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PATH=$PATH:/root/.poetry/bin/:/root/.pyenv/bin/

RUN pyenv install 3.9.2 && \
    ln -s /root/.pyenv/versions/3.9.2/bin/python /usr/bin/python3.9

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . .

ENTRYPOINT ["make"]
