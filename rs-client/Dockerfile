FROM rust:1 as builder

RUN USER=root cargo new --bin rs-client
WORKDIR /rs-client
COPY ./Cargo.toml ./Cargo.toml
COPY ./src ./src
RUN cargo build --release


FROM debian:buster-slim
ARG APP=/usr/src/app

WORKDIR ${APP}

ARG host
ARG port
ARG id
ARG let
ARG lan
ARG topic

CMD ["./rs-client", "--host $host", "--port $port", "--id $id", "--let $let", "--lan $lan", "--topic $topic"]
