# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN apt update && \
    apt install -y gcc libpq-dev && \
    pip3 install -r requirements.txt

CMD [ "python3", "msqt_to_tsdb.py"]