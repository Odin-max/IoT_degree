import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv

load_dotenv()


ca_cert_path = os.getenv("CA_CERT_PATH")
client_cert_path = os.getenv("CLIENT_CERT_PATH")
client_key_path = os.getenv("CLIENT_KEY_PATH")


def publish_data_from_json(file_path, mqtt_broker, mqtt_port, topic):
    """
    Читає JSON-файл і відправляє кожен запис на MQTT брокер.
    """
    with open(file_path, "r") as file:
        data = json.load(file)["iot_report"]
    if not data:
        raise ValueError("JSON-файл порожній або не містить iot_report.")


    client = mqtt.Client()
    client.tls_set(
        ca_certs=ca_cert_path,
        certfile=client_cert_path,
        keyfile=client_key_path
    )
    client.connect(mqtt_broker, mqtt_port)

    for entry in data:
        client.publish(topic, json.dumps(entry))
        print(f"Відправлено дані на MQTT брокер: {entry['device_id']}")

    client.disconnect()

if __name__ == "__main__":
    mqtt_broker = os.getenv("MQTT_BROKER")
    mqtt_port = int(os.getenv("MQTT_PORT"))
    topic = os.getenv("MQTT_TOPIC")

    # Відправка даних
    publish_data_from_json("iot_report.json", mqtt_broker, mqtt_port, topic)
