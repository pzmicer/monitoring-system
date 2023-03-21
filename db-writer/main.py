import argparse
import json
import logging
import sys
from datetime import datetime
import os

import paho.mqtt.client as mqtt
import psycopg2


logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

args = argparse.Namespace
db_connection: str = ""


def main():
    global args
    args = parse_args()

    global db_connection
    db_connection = "postgres://{}:{}@{}:{}/{}".format(
        args.db_username, 
        args.db_password, 
        args.db_host,
        args.db_port, 
        args.db_database)
    logger.debug("Database connection: {}".format(db_connection))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print(args.mqtt_host, args.mqtt_port)
    client.connect(args.mqtt_host, args.mqtt_port, 60)

    client.loop_forever()


# CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logger.debug("Connected with result code {}".format(str(rc)))
    client.subscribe(args.mqtt_topic)


# PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logger.debug("Topic: {}, Message Payload: {}".format(msg.topic, str(msg.payload)))
    publish_message_to_db(msg)


def date_converter(o):
    if isinstance(o, datetime):
        return o.__str__()


def publish_message_to_db(message_json):
    message = json.loads(message_json.payload)
    # logger.debug("message.payload: {}".format(json.dumps(message, default=date_converter)))

    sql = """INSERT INTO sensor_data(
                    device_id, 
                    time,
                    temp_c,
                    humidity
                )
                VALUES (%s, %s, %s, %s);"""

    data = (
        message["device_id"], 
        message["time"], 
        message["data"]["temp_c"],
        message["data"]["humidity"]
    )

    try:
        with psycopg2.connect(db_connection, connect_timeout=3) as conn:
            with conn.cursor() as curs:
                try:
                    curs.execute(sql, data)
                except psycopg2.Error as error:
                    logger.error("Exception: {}".format(error.pgerror))
                except Exception as error:
                    logger.error("Exception: {}".format(error))
    except psycopg2.OperationalError as error:
        logger.error("Exception: {}".format(error.pgerror))
    finally:
        conn.close()


def parse_args():
    parser = argparse.ArgumentParser(description='Script arguments')
    parser.add_argument('--mqtt_topic', help='MQTT Broker topic')
    parser.add_argument('--mqtt_host', help='MQTT Broker host', default='localhost')
    parser.add_argument('--mqtt_port', help='MQTT Broker port', type=int, default=1881)
    parser.add_argument('--db_host', help='DB host', default='localhost')
    parser.add_argument('--db_port', help='DB port', type=int, default=5432)
    parser.add_argument('--db_username', help='DB username')
    parser.add_argument('--db_password', help='DB password')
    parser.add_argument('--db_database', help='DB database')

    return parser.parse_args()


if __name__ == "__main__":
    main()