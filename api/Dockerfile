# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

WORKDIR /code

COPY requirements.txt requirements.txt

RUN apt update && \
    apt install -y gcc libpq-dev && \
    pip3 install -r requirements.txt

COPY app app
EXPOSE 8000
CMD uvicorn app.main:app --host 0.0.0.0 --root-path /api