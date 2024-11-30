from celery import Celery
from celery.schedules import crontab
import sys
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

# Додайте періодичні завдання через beat_schedule
app.conf.beat_schedule = {
    "update-iot-data-every-5-minutes": {
        "task": "celery_app.update_iot_data",
        "schedule": crontab(minute="*/5"),  # Кожні 5 хвилин
    },
}

@app.task
def update_iot_data():
    """
    Оновлює випадкові дані IoT у базі даних кожні 5 хвилин.
    """
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    from save_to_postgres import IoTData
    import random

    DATABASE_URL = "postgresql://postgres:PG13@localhost/iot_analysis_db"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Отримуємо всі існуючі записи
        records = session.query(IoTData).all()

        if not records:
            print("База даних порожня. Немає записів для оновлення.")
            return

        for record in records:
            # Оновлюємо лише випадкові поля
            record.temperature_c = round(random.uniform(-10, 50), 2)
            record.humidity = round(random.uniform(0, 100), 2)
            record.data_rate_kbps = random.randint(100, 10000)

        session.commit()
        print(f"Оновлено {len(records)} записів.")
    except Exception as e:
        session.rollback()
        print(f"Помилка під час оновлення: {e}")
    finally:
        session.close()

# celery -A celery_app worker --pool=solo --loglevel=info
# celery -A celery_app beat --loglevel=info
