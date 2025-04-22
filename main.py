import os
from dotenv import load_dotenv
import influxdb_client as influxdb
from influxdb_client.client.write_api import SYNCHRONOUS
from paho.mqtt import client as mqtt
from datetime import datetime

load_dotenv()
influxdb_url = os.getenv("INFLUXDB_URL", default="http://localhost:8086")
influxdb_token = os.getenv("INFLUXDB_TOKEN", default="my-token")
influxdb_org = os.getenv("INFLUXDB_ORG", default="em")
influxdb_bucket = os.getenv("INFLUXDB_BUCKET", default="em")
mqtt_broker = os.getenv("MQTT_BROKER", default="localhost")
mqtt_port = int(os.getenv("MQTT_PORT", default=1883))
mqtt_client_id = os.getenv("MQTT_CLIENT_ID", default="mqtt-data-logger-v0")
mqtt_topic = os.getenv("MQTT_TOPIC", default="em/#")


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8").split(" ")

        if len(payload) < 3:
            timestamp = int(datetime.now().timestamp())
        else:
            timestamp = int(payload[2])
        timestamp *= 1000000000

        record = " ".join([payload[0], payload[1], str(timestamp)])
        with influxdb_client.write_api(write_options=SYNCHRONOUS) as writer:
            writer.write(bucket=influxdb_bucket, org=influxdb_org, record=record)
    except Exception as e:
        print(f"Error processing message: {e}")


if __name__ == "__main__":
    influxdb_client = influxdb.InfluxDBClient(
        url=influxdb_url, token=influxdb_token, org=influxdb_org
    )

    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, mqtt_client_id)
    mqtt_client.connect(mqtt_broker, mqtt_port, 60)
    mqtt_client.subscribe(mqtt_topic)
    mqtt_client.on_message = on_message
    mqtt_client.loop_forever()
