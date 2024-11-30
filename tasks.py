from celery_app import app

# Тільки одна задача для оновлення
@app.task
def update_iot_data():
    """
    Завдання для оновлення існуючих даних у базі.
    """
    from celery_app import update_iot_data
    update_iot_data()
