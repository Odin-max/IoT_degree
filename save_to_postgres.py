from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import json
import os
from datetime import datetime

# Завантаження змінних середовища
load_dotenv()

# SQLAlchemy базові налаштування
Base = declarative_base()

# Отримання або генерація ключа для шифрування
encryption_key = os.getenv("FERNET_KEY")
if not encryption_key:
    encryption_key = Fernet.generate_key().decode()
    with open(".env", "a") as env_file:
        env_file.write(f"FERNET_KEY={encryption_key}\n")
    print("Новий ключ шифрування збережено у .env файлі.")

cipher = Fernet(encryption_key.encode())

# Функції для шифрування та розшифрування
def encrypt_data(data):
    """Шифрує дані."""
    json_data = json.dumps(data)  # Перетворення на JSON-рядок
    encrypted = cipher.encrypt(json_data.encode())
    return encrypted.decode()  # Збереження як текст

def decrypt_data(encrypted_data):
    """Розшифровує дані."""
    decrypted = cipher.decrypt(encrypted_data.encode())
    return json.loads(decrypted.decode())

# Модель IoT
class IoTData(Base):
    __tablename__ = "iot_data"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    last_updated = Column(DateTime, nullable=False)
    device_id = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    mac_address = Column(String, nullable=False)
    connection_status = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    critical_data = Column(Text, nullable=False)  # Тип змінено на TEXT

# Налаштування бази даних
DATABASE_URL = "postgresql://postgres:PG13@localhost/iot_analysis_db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Функція для завантаження даних
def load_data_to_db(file_path):
    """
    Завантаження IoT-даних з JSON у базу з шифруванням.
    """
    with open(file_path, "r") as file:
        data = json.load(file)["iot_report"]

    for entry in data:
        encrypted_first_name = encrypt_data(entry["first_name"])
        encrypted_last_name = encrypt_data(entry["last_name"])
        encrypted_critical_data = encrypt_data(entry["critical_data"])

        db_entry = IoTData(
            timestamp=entry["timestamp"],
            last_updated=entry["last_updated"],
            device_id=entry["device_id"],
            ip_address=entry["ip_address"],
            mac_address=entry["mac_address"],
            connection_status=entry["connection_status"],
            device_type=entry["device_type"],
            manufacturer=entry["manufacturer"],
            first_name=encrypted_first_name,
            last_name=encrypted_last_name,
            critical_data=encrypted_critical_data,
        )
        session.add(db_entry)

    session.commit()
    print(f"Дані успішно збережені. Кількість записів: {len(data)}")

# Виконання
if __name__ == "__main__":
    load_data_to_db("iot_report.json")
