from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import json
from datetime import datetime

# SQLAlchemy базові налаштування
Base = declarative_base()

class IoTData(Base):
    __tablename__ = "iot_data"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)  # Використання DateTime
    last_updated = Column(DateTime, nullable=False)
    device_id = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    mac_address = Column(String, nullable=False)
    protocol = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    encryption = Column(String, nullable=False)
    auth_status = Column(String, nullable=False)
    login_attempts = Column(Integer, nullable=False)
    data_rate_kbps = Column(Float, nullable=False)
    anomaly = Column(String, nullable=True)
    # Нові поля
    temperature_c = Column(Float, nullable=True)  # Температура в градусах Цельсія
    humidity = Column(Float, nullable=True)       # Вологість у відсотках

# Налаштування бази даних
DATABASE_URL = "postgresql://postgres:PG13@localhost/iot_analysis_db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Функція для завантаження JSON-даних у базу
def load_data_to_db(file_path):
    """
    Завантаження IoT-даних з JSON-файлу до PostgreSQL.
    """
    with open(file_path, "r") as file:
        data = json.load(file)["iot_report"]

    for entry in data:
        print("Processing entry:", entry)  # Додайте дебаг-лог для перевірки
        db_entry = IoTData(
            timestamp=entry["timestamp"],  # Використовуємо [] замість .get()
            last_updated = entry["last_updated"],
            device_id=entry["device_id"],
            ip_address=entry["ip_address"],
            mac_address=entry["mac_address"],
            protocol=entry["protocol"],
            port=entry["port"],
            encryption=entry["encryption"],
            auth_status=entry["auth_status"],
            login_attempts=entry["login_attempts"],
            data_rate_kbps=entry["data_rate_kbps"],
            anomaly=entry["anomaly"],
            temperature_c=entry["temperature_celsius"],  # Використовуємо [] замість .get()
            humidity=entry["humidity_percent"],            # Використовуємо [] замість .get()
        )
        session.add(db_entry)

    session.commit()
    print(f"Дані успішно збережені. Кількість записів: {len(data)}")

# Виконання
if __name__ == "__main__":
    load_data_to_db("iot_report.json")
