import sys
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from subscriber import IoTData, encrypt_data
from datetime import datetime
from celery import Celery
from celery.schedules import crontab
from pytz import timezone
import paho.mqtt.client as mqtt
import json
from dotenv import load_dotenv
import random
from faker import Faker

# Завантаження змінних середовища
load_dotenv()

# Ініціалізація Faker для оновлення імен
fake = Faker()

# Додавання шляху до проекту
sys.path.append('D:/PythonProjects/Iot_degree')


# Створення інстансу Celery
app = Celery(
    "iot_project",
    broker=os.getenv("broker_url"),  # URL до Redis
    backend=os.getenv("backend_url")  # URL для результатів
)

# Додаткові конфігурації
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    timezone="Europe/Kyiv",  # Встановлення київського часу
    enable_utc=True,
)

# Beat schedule
app.conf.beat_schedule = {
    "update-iot-data-every-5-minutes": {
        "task": "celery_app.update_iot_data",
        "schedule": crontab(minute="*/1"),  # Кожні 5 хвилин
    },
}

# Налаштування шляху до лог-файлу
LOG_DIR = "log"
LOG_FILE = os.path.join(LOG_DIR, "iot_data_update.log")

# Створення папки для логів, якщо вона не існує
os.makedirs(LOG_DIR, exist_ok=True)

# Налаштування MQTT
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = os.getenv("MQTT_PORT")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

# Функція для запису логів
def write_log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")
    print(message)  # Додатково виводимо в консоль

# Функція для публікації даних через MQTT
def publish_to_mqtt(payload):
    """
    Публікує дані в MQTT брокер.
    """
    client = mqtt.Client()
    try:
        client.tls_set(
            ca_certs="C:/mosquitto/certs/ca.crt",  # Сертифікат центру сертифікації (CA)
            certfile="C:/mosquitto/certs/client.crt",  # Клієнтський сертифікат
            keyfile="C:/mosquitto/certs/client.key"    # Приватний ключ клієнта
        )
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.publish(MQTT_TOPIC, json.dumps(payload))
        write_log(f"Дані передано до MQTT брокера: {payload['device_id']}")
    except Exception as e:
        write_log(f"Помилка публікації до MQTT: {e}")
    finally:
        client.disconnect()

@app.task
def update_iot_data():
    """
    Оновлює випадкові дані IoT у базі кожні 5 хвилин і публікує їх у MQTT брокер.
    """
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    kyiv_time = timezone("Europe/Kyiv")

    try:
        write_log("===== Starting Update Task =====")
        records = session.query(IoTData).all()
        updated_count = 0

        for record in records:
            # Оновлюємо статус підключення
            record.connection_status = "Connected" if random.random() < 0.9 else "Disconnected"

            if record.connection_status == "Disconnected":
                # Якщо пристрій не підключений, очищуємо критичні дані
                record.critical_data = encrypt_data({})
                write_log(f"Пристрій {record.device_id} відключений.")
                continue

            # Оновлення імені та прізвища
            first_name = fake.first_name()
            last_name = fake.last_name()
            record.first_name = encrypt_data(first_name)
            record.last_name = encrypt_data(last_name)

             # Оновлення критичних даних залежно від типу пристрою
            critical_data = {}
            device_type = record.device_type

            if device_type == "Heart Rate Monitor":
                critical_data["heart_rate"] = random.randint(40, 180)  # bpm
            elif device_type == "Blood Pressure Monitor":
                critical_data["blood_pressure"] = f"{random.randint(90, 180)}/{random.randint(60, 120)}"  # mmHg
            elif device_type == "Glucose Meter":
                critical_data["glucose_level_mg_dL"] = random.randint(70, 200)  # mg/dL
            elif device_type == "Infusion Pump":
                critical_data["infusion_rate_mL_h"] = round(random.uniform(0.1, 500.0), 2)  # mL/h
            elif device_type == "ECG Monitor":
                critical_data["ecg_readings"] = [round(random.uniform(-1.0, 1.0), 2) for _ in range(10)]  # Simulated ECG readings
            elif device_type == "Smart Bed":
                critical_data["patient_weight_kg"] = random.randint(40, 200)  # kg
                critical_data["bed_angle_deg"] = round(random.uniform(0, 45), 1)  # degrees
            elif device_type == "Ventilator":
                critical_data["oxygen_saturation_percent"] = round(random.uniform(80.0, 100.0), 2)  # %
                critical_data["respiratory_rate_bpm"] = random.randint(10, 30)  # breaths per minute
            elif device_type == "Wearable Fitness Tracker":
                critical_data["steps_count"] = random.randint(0, 20000)  # steps
                critical_data["calories_burned_kcal"] = round(random.uniform(0.0, 5000.0), 2)


            # Шифруємо критичні дані
            record.critical_data = encrypt_data(critical_data)

            # Оновлюємо поле `last_updated`
            record.last_updated = datetime.now(kyiv_time)

            updated_count += 1

            # Підготовка даних для публікації
            payload = {
                "timestamp": record.timestamp.isoformat(),
                "last_updated": record.last_updated.isoformat(),
                "device_id": record.device_id,
                "ip_address": record.ip_address,
                "mac_address": record.mac_address,
                "connection_status": record.connection_status,
                "device_type": record.device_type,
                "manufacturer": record.manufacturer,
                "first_name": first_name,
                "last_name": last_name,
                "critical_data": critical_data,
            }

            # Публікуємо в MQTT брокер
            publish_to_mqtt(payload)

            log_message = (
                f"Updated Record ID: {record.id} | Last Updated: {record.last_updated} | Critical Data: {critical_data}"
            )
            write_log(log_message)

        session.commit()
        write_log(f"Оновлено {updated_count} записів у базі.")
    except Exception as e:
        session.rollback()
        write_log(f"Помилка під час оновлення: {e}")
    finally:
        session.close()








# mosquitto -c C:\mosquitto\mosquitto.conf -v
# celery -A celery_app worker --pool=solo --loglevel=info
# celery -A celery_app beat --loglevel=info
