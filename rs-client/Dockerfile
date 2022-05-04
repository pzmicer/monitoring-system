FROM rust:1 as builder

RUN cargo new --bin rs-client
WORKDIR /rs-client
COPY ./Cargo.toml ./Cargo.toml
COPY ./src ./src
RUN cargo build --release


FROM debian:buster-slim
WORKDIR /root/
COPY --from=builder /rs-client/target/release/rs-client .

ARG host
ARG port
ARG id
ARG let
ARG lan
ARG topic

CMD ["./rs-client", "--host $host", "--port $port", "--id $id", "--let $let", "--lan $lan", "--topic $topic"]
