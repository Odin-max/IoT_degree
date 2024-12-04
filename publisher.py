import paho.mqtt.client as mqtt
import json
import os


def publish_data_from_json(file_path, mqtt_broker, mqtt_port, topic):
    """
    Читає JSON-файл і відправляє кожен запис на MQTT брокер.
    """
    with open(file_path, "r") as file:
        data = json.load(file)["iot_report"]
    if not data:
        raise ValueError("JSON-файл порожній або не містить iot_report.")


    client = mqtt.Client()
    client.connect(mqtt_broker, mqtt_port)

    for entry in data:
        client.publish(topic, json.dumps(entry))
        print(f"Відправлено дані на MQTT брокер: {entry['device_id']}")

    client.disconnect()

if __name__ == "__main__":
    mqtt_broker = "127.0.0.1"
    mqtt_port = 1883
    topic = "iot/healthcare"

    # Відправка даних
    publish_data_from_json("iot_report.json", mqtt_broker, mqtt_port, topic)
