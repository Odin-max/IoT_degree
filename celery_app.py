import sys
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from save_to_postgres import IoTData
import random
from datetime import datetime
from celery import Celery
from celery.schedules import crontab
from pytz import timezone

# Додавання шляху до проекту
sys.path.append('D:/PythonProjects/Iot_degree')

# Створення інстансу Celery
app = Celery(
    "iot_project",
    broker="redis://localhost:6379/0",  # URL до Redis
    backend="redis://localhost:6379/0"  # URL для результатів
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
        "schedule": crontab(minute="*/1"),  # Кожні 1 хвилину для тестування
    },
}

# Налаштування шляху до лог-файлу
LOG_DIR = "log"
LOG_FILE = os.path.join(LOG_DIR, "iot_data_update.log")

# Створення папки для логів, якщо вона не існує
os.makedirs(LOG_DIR, exist_ok=True)

# Функція для запису логів
def write_log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")
    print(message)  # Додатково виводимо в консоль


@app.task
def update_iot_data():
    """
    Оновлює випадкові дані IoT у базі кожні 5 хвилин.
    """
    DATABASE_URL = "postgresql://postgres:PG13@localhost/iot_analysis_db"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Встановлення часу в київському часовому поясі
    kyiv_time = timezone("Europe/Kyiv")

    try:
        write_log("===== Starting Update Task =====")
        # Отримання всіх записів
        records = session.query(IoTData).all()

        updated_count = 0

        for record in records:
            # Зберігаємо старі значення для логування
            old_temperature = record.temperature_c
            old_humidity = record.humidity
            old_data_rate = record.data_rate_kbps
            old_anomaly = record.anomaly
            old_login_attempts = record.login_attempts
            old_auth_status = record.auth_status
            old_last_updated = record.last_updated

            # Оновлення випадкових значень
            record.temperature_c = round(random.uniform(-10, 50), 2)
            record.humidity = round(random.uniform(0, 100), 2)
            record.data_rate_kbps = random.randint(100, 10000)
            record.anomaly = "None" if random.random() < 0.9 else random.choice(
                ["High Activity", "Packet Loss", "DoS Attempt"]
            )
            record.login_attempts = 1 if random.random() < 0.9 else random.randint(2, 10)
            record.auth_status = "Failure" if random.random() < 0.05 else "Success"

            # Оновлюємо поле `last_updated` до поточного київського часу
            record.last_updated = datetime.now(kyiv_time)

            updated_count += 1

            # Логування оновлення
            log_message = (
                f"Updated Record ID: {record.id} | "
                f"Temperature: {old_temperature} -> {record.temperature_c}, "
                f"Humidity: {old_humidity} -> {record.humidity}, "
                f"Data Rate: {old_data_rate} -> {record.data_rate_kbps}, "
                f"Anomaly: {old_anomaly} -> {record.anomaly}, "
                f"Login Attempts: {old_login_attempts} -> {record.login_attempts}, "
                f"Auth Status: {old_auth_status} -> {record.auth_status}, "
                f"Last Updated: {old_last_updated} -> {record.last_updated}"
            )
            write_log(log_message)

        session.commit()
        write_log(f"Оновлено {updated_count} записів у базі.")
    except Exception as e:
        session.rollback()
        write_log(f"Помилка під час оновлення: {e}")
    finally:
        session.close()








# celery -A celery_app worker --pool=solo --loglevel=info
# celery -A celery_app beat --loglevel=info
