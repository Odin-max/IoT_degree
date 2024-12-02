import paho.mqtt.client as mqtt
import json

def publish_test_message():
    """
    Публікує тестове повідомлення на тему 'iot/healthcare'.
    """
    # Створення клієнта MQTT
    client = mqtt.Client()
    
    # Підключення до брокера
    client.connect("127.0.0.1", 1883, 60)  # Адреса брокера і порт

    # Тестове повідомлення
    test_payload = {
        "timestamp": "2024-12-02T12:34:56",
        "last_updated": "2024-12-02T12:34:56",
        "device_id": "Device_1234",
        "ip_address": "192.168.0.1",
        "mac_address": "00:1A:2B:3C:4D:5E",
        "connection_status": "Connected",
        "device_type": "Heart Rate Monitor",
        "manufacturer": "HealthPro Systems",
        "first_name": "John",
        "last_name": "Doe",
        "critical_data": {
            "heart_rate": 72,
            "blood_pressure": None,
            "glucose_level_mg_dL": None,
            "oxygen_saturation_percent": None
        }
    }

    # Публікація повідомлення
    client.loop_start()
    client.publish("test/topic", json.dumps(test_payload))
    client.loop_stop()
    print("Повідомлення відправлено на тему 'iot/healthcare'.")

    # Закриття з'єднання
    client.disconnect()

if __name__ == "__main__":
    publish_test_message()
