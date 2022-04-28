import argparse
import json
import logging
import sys
import time
from datetime import datetime

import paho.mqtt.client as client
import paho.mqtt.publish as publish
from pytz import timezone
import random


logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    args = parse_args()
    publish_message_to_db(args)


def get_readings(args):
    data_temp_c = random.uniform(20.0, 30.0)
    data_pressure_hpa = random.uniform(800.0, 1200.0)
    data_wind_speed_ms = random.uniform(2.0, 15.0)

    message = {
        "device_id": args.id,
        "time": datetime.now(timezone("UTC")),
        "data": {
            "temp_c": data_temp_c,
            "pressure_hpa": data_pressure_hpa,
            "wind_speed_ms": data_wind_speed_ms,
        },
        "coords": {
            "lat": args.lat,
            "lon": args.lon,
        }
    }

    return message


def date_converter(o):
    if isinstance(o, datetime):
        return o.__str__()


def publish_message_to_db(args):
    while True:
        message = get_readings(args)
        message_json = json.dumps(message, default=date_converter, sort_keys=True,
                                  indent=None, separators=(',', ':'))
        logger.debug(message_json)

        try:
            publish.single(args.topic, payload=message_json, qos=0, retain=False, 
                           hostname=args.host, port=args.port, client_id="", 
                           keepalive=60, will=None, auth=None, tls=None, 
                           protocol=client.MQTTv311, transport="tcp")
        except Exception as error:
            logger.error("Exception: {}".format(error))
        finally:
            time.sleep(args.frequency)


# Read in command-line parameters
def parse_args():
    parser = argparse.ArgumentParser(description='Script arguments')
    parser.add_argument('--id', help='Device id')
    parser.add_argument('--lat', help='Latitude')
    parser.add_argument('--lon', help='Longitude')
    parser.add_argument('--host', help='Mosquitto host', default='localhost')
    parser.add_argument('--port', help='Mosquitto port', type=int, default=1883)
    parser.add_argument('--topic', help='Mosquitto topic', default='paho/test')
    parser.add_argument('--frequency', help='Message frequency in seconds', type=int, default=5)

    return parser.parse_args()


if __name__ == "__main__":
    main()