# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt update && \
    apt install -y gcc libpq-dev && \
    pip3 install -r requirements.txt

COPY main.py main.py

CMD python3 main.py \
    --mqtt_topic $MOSQUITTO_TOPIC \
    --mqtt_host $MOSQUITTO_HOST \
    --mqtt_port $MOSQUITTO_PORT \
    --db_host $DATABASE_HOST \
    --db_port $DATABASE_PORT \
    --db_username $POSTGRES_USER \
    --db_password $POSTGRES_PASSWORD \
    --db_database $POSTGRES_DB