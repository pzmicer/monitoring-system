# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN apt update && \
    apt install -y gcc libpq-dev && \
    pip3 install -r requirements.txt

CMD python3 main.py \
    --msqt_topic $MOSQUITTO_TOPIC \
    --msqt_host $MOSQUITTO_HOST \
    --msqt_port $MOSQUITTO_PORT \
    --ts_host $DATABASE_HOST \
    --ts_port $DATABASE_PORT \
    --ts_username $POSTGRES_USER \
    --ts_password $POSTGRES_PASSWORD \
    --ts_database $POSTGRES_DB

# CMD [ "env" ]