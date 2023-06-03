import time
import board
from adafruit_htu21d import HTU21D

import paho.mqtt.publish as publish

import os, argparse, json
from datetime import datetime, timezone


parser = argparse.ArgumentParser()
parser.add_argument("host", help="MQTT broker host (IP address or DNS name)")
parser.add_argument("-p", "--port", type=int, help="MQTT broker port (default is 1883)", default=1883)
parser.add_argument("-t", "--topic", help="MQTT topic name")
parser.add_argument("-i", "--id", type=int, help="Device id")
args = parser.parse_args()

i2c = board.I2C()
sensor = HTU21D(i2c)

json_payload = json.dumps({
    "device_id":  args.id,
    "time": str(datetime.now(timezone.utc)),
    "data": {
        "temp_c": sensor.temperature,
        "hum": sensor.relative_humidity,
    }
})
print(json_payload)

publish.single(args.topic, json_payload, qos=1, hostname=args.host, port=args.port)
