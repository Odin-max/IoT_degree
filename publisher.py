import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
from validator import validate_payload  # Імпортуємо валідатор
import time
import psutil

load_dotenv()

# Шляхи до сертифікатів
ca_cert_path = os.getenv("CA_CERT_PATH")
client_cert_path = os.getenv("CLIENT_CERT_PATH")
client_key_path = os.getenv("CLIENT_KEY_PATH")

def publish_data_from_json(file_path, mqtt_broker, mqtt_port, topic):
    """
    Читає JSON-файл і відправляє кожен запис на MQTT брокер після перевірки валідатором.
    """
    initial_cpu = psutil.cpu_percent(interval=0.1)
    initial_memory = psutil.virtual_memory().percent
    start_time = time.time()

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
        try:
            # Використовуємо валідатор перед публікацією
            validate_payload(entry)
            client.publish(topic, json.dumps(entry))
            print(f"Відправлено дані на MQTT брокер: {entry['device_id']}")
        except ValueError as e:
            print(f"Помилка валідації даних для пристрою {entry.get('device_id', 'невідомий')}: {e}")

    client.disconnect()
    final_cpu = psutil.cpu_percent(interval=0.1)
    final_memory = psutil.virtual_memory().percent
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Функція виконувалася: {elapsed_time} секунд")  
    print(f"Використання CPU до виконання: {initial_cpu}%")
    print(f"Використання CPU після виконання: {final_cpu}%")
    print(f"Використання пам'яті до виконання: {initial_memory}%")
    print(f"Використання пам'яті після виконання: {final_memory}%")
     
if __name__ == "__main__":
    mqtt_broker = os.getenv("MQTT_BROKER")
    mqtt_port = int(os.getenv("MQTT_PORT"))
    topic = os.getenv("MQTT_TOPIC")

    # Відправка даних
    publish_data_from_json("iot_report.json", mqtt_broker, mqtt_port, topic)
