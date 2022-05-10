FROM rust:1 as builder

RUN cargo new --bin rs-client
WORKDIR /rs-client
COPY ./Cargo.toml ./Cargo.toml
COPY ./src ./src
RUN cargo build --release


FROM debian:buster-slim
WORKDIR /root/
COPY --from=builder /rs-client/target/release/rs-client .

CMD [ "./rs-client", \
    "--host $MOSQUITTO_HOST", \
    "--port $MOSQUITTO_PORT", \
    "--id $DEVICE_ID", \
    "--lat $LAT", \
    "--lon $LON", \
    "--topic $MOSQUITTO_TOPIC" ]
