use chrono;
use clap::Parser;
use rumqttc::{Client, MqttOptions, QoS};
use serde_json::json;
use std::thread;
use std::time::Duration;

use rand::prelude::*;

#[derive(Parser, Debug)]
#[clap(allow_negative_numbers = true)]
struct Args {
    #[clap(long)]
    id: String,

    #[clap(long)]
    lat: f64,

    #[clap(long)]
    lon: f64,

    #[clap(long)]
    topic: String,

    #[clap(long, default_value_t = String::from("localhost"))]
    host: String,

    #[clap(long)]
    port: u16,
}

fn get_data(args: &Args) -> String {
    let mut thread_rng = rand::thread_rng();

    let temp_c: f64 = thread_rng.gen_range(10.0..30.0);
    let pressure_hpa: f64 = thread_rng.gen_range(800.0..1200.0);
    let wind_speed_ms: f64 = thread_rng.gen_range(2.0..15.0);

    let time = chrono::offset::Utc::now().to_string();

    let data = json!({
        "device_id": args.id,
        "time": time,
        "data": {
            "temp_c": temp_c,
            "pressure_hpa": pressure_hpa,
            "wind_speed_ms": wind_speed_ms,
        },
        "coords": {
            "lat": args.lat,
            "lon": args.lon,
        },
    });

    println!("{}", data);

    data.to_string()
}

fn main() {
    let args = Args::parse();

    let mut mqttoptions = MqttOptions::new("rumqtt-client", &args.host, args.port);
    mqttoptions.set_keep_alive(Duration::from_secs(10));

    let (mut client, mut connection) = Client::new(mqttoptions, 1);

    // loop {
    //     // client.subscribe(&args.topic, QoS::AtMostOnce).unwrap();
    //     client.publish(&args.topic, QoS::AtLeastOnce, false, get_data(&args)).unwrap();
    //     thread::sleep(Duration::from_secs(5));
    // }

    thread::spawn(move || loop {
        client
            .publish(&args.topic, QoS::AtLeastOnce, false, get_data(&args))
            .unwrap();
        thread::sleep(Duration::from_secs(5));
    });

    // Iterate to poll the eventloop for connection progress
    for (_, notification) in connection.iter().enumerate() {
        println!("Notification = {:?}", notification);
    }
}
