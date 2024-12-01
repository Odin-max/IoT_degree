from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
import json

# SQLAlchemy базові налаштування
Base = declarative_base()

class IoTData(Base):
    __tablename__ = "iot_data"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)  # Час створення запису
    last_updated = Column(DateTime, nullable=False)  # Час останнього оновлення
    first_name = Column(String, nullable=False)  # Ім'я користувача
    last_name = Column(String, nullable=False)  # Прізвище користувача
    device_id = Column(String, nullable=False)  # Унікальний ID пристрою
    device_type = Column(String, nullable=False)  # Тип пристрою
    manufacturer = Column(String, nullable=False)  # Виробник пристрою
    ip_address = Column(String, nullable=False)  # IP-адреса пристрою
    mac_address = Column(String, nullable=False)  # MAC-адреса пристрою
    connection_status = Column(String, nullable=False)  # Статус підключення
    critical_data = Column(JSON, nullable=True)  # Специфічні дані пристрою

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
            timestamp=entry["timestamp"],
            last_updated=entry["last_updated"],
            first_name=entry["first_name"],
            last_name=entry["last_name"],
            device_id=entry["device_id"],
            device_type=entry["device_type"],
            manufacturer=entry["manufacturer"],
            ip_address=entry["ip_address"],
            mac_address=entry["mac_address"],
            connection_status=entry["connection_status"],
            critical_data=entry["critical_data"],  # JSON-дані специфічні для пристрою
        )
        session.add(db_entry)

    session.commit()
    print(f"Дані успішно збережені. Кількість записів: {len(data)}")

# Виконання
if __name__ == "__main__":
    load_data_to_db("iot_report.json")
