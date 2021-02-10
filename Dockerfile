FROM python:3.9-slim-buster

RUN apt update && \
    apt install --yes inotify-tools make && \
    rm -rf /var/lib/apt/lists/*

RUN apt update && apt install --yes gcc
RUN apt install --yes build-essential

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["make"]
