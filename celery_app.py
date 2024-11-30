import sys
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from save_to_postgres import IoTData
import random
from celery import Celery
from celery.schedules import crontab

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
    timezone="UTC",
    enable_utc=True,
)

# Beat schedule
app.conf.beat_schedule = {
    "update-iot-data-every-5-minutes": {
        "task": "celery_app.update_iot_data",
        "schedule": crontab(minute="*/1"),  # Кожні 1 хвилину для тестування
    },
}

# Налаштування логування
log_file_path = "iot_data_update.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path, mode="a", encoding="utf-8"),
        logging.StreamHandler(),  # Для виведення в консоль
    ],
)

logger = logging.getLogger(__name__)  # Ініціалізація логера для модуля

@app.task
def update_iot_data():
    """
    Оновлює випадкові дані IoT у базі кожні 5 хвилин.
    """
    from datetime import datetime

    DATABASE_URL = "postgresql://postgres:PG13@localhost/iot_analysis_db"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
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

            # Оновлюємо поле `last_updated` до поточного часу
            record.last_updated = datetime.utcnow()

            updated_count += 1

            # Логування оновлення
            logger.info(
                f"Updated Record ID: {record.id} | "
                f"Temperature: {old_temperature} -> {record.temperature_c}, "
                f"Humidity: {old_humidity} -> {record.humidity}, "
                f"Data Rate: {old_data_rate} -> {record.data_rate_kbps}, "
                f"Anomaly: {old_anomaly} -> {record.anomaly}, "
                f"Login Attempts: {old_login_attempts} -> {record.login_attempts}, "
                f"Auth Status: {old_auth_status} -> {record.auth_status}, "
                f"Last Updated: {old_last_updated} -> {record.last_updated}"
            )

        session.commit()
        logger.info(f"Оновлено {updated_count} записів у базі.")
    except Exception as e:
        session.rollback()
        logger.error(f"Помилка під час оновлення: {e}")
    finally:
        session.close()






# celery -A celery_app worker --pool=solo --loglevel=info
# celery -A celery_app beat --loglevel=info
