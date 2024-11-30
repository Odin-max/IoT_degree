from celery import Celery
from celery.schedules import crontab
from celery_app import app

# Додайте лише задачу для оновлення даних
app.conf.beat_schedule = {
    "update-iot-data-every-1-minutes": {
        "task": "tasks.update_iot_data",
        "schedule": crontab(minute="*/5"),
    },
}
