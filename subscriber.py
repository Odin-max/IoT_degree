from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import json
import paho.mqtt.client as mqtt

# Завантаження змінних середовища
load_dotenv()

# SQLAlchemy базові налаштування
Base = declarative_base()

# Отримання ключа для шифрування
encryption_key = os.getenv("FERNET_KEY")
if not encryption_key:
    raise ValueError("FERNET_KEY не знайдено у .env файлі.")
cipher = Fernet(encryption_key.encode())

# Функції для шифрування та розшифрування
def encrypt_data(data):
    """Шифрує дані."""
    json_data = json.dumps(data)
    encrypted = cipher.encrypt(json_data.encode())
    return encrypted.decode()

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
    critical_data = Column(Text, nullable=False)

# Налаштування бази даних
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

# Обробник повідомлень MQTT
def on_message(client, userdata, message):
    """
    Обробляє отримане повідомлення від MQTT та зберігає в базу даних.
    """
    session = Session()
    try:
        # Отримуємо та десеріалізуємо дані
        payload = json.loads(message.payload.decode("utf-8"))
        print(f"Отримано дані: {payload}")

        # Шифруємо поля перед збереженням
        encrypted_first_name = encrypt_data(payload["first_name"])
        encrypted_last_name = encrypt_data(payload["last_name"])
        encrypted_critical_data = encrypt_data(payload["critical_data"])

        # Створюємо запис для бази
        db_entry = IoTData(
            timestamp=payload["timestamp"],
            last_updated=payload["last_updated"],
            device_id=payload["device_id"],
            ip_address=payload["ip_address"],
            mac_address=payload["mac_address"],
            connection_status=payload["connection_status"],
            device_type=payload["device_type"],
            manufacturer=payload["manufacturer"],
            first_name=encrypted_first_name,
            last_name=encrypted_last_name,
            critical_data=encrypted_critical_data,
        )
        session.add(db_entry)
        session.commit()
        print(f"Збережено дані для пристрою {payload['device_id']}.")
    except Exception as e:
        session.rollback()
        print(f"Помилка під час збереження: {e}")
    finally:
        session.close()

# Налаштування MQTT клієнта
def receive_data_from_mqtt(mqtt_broker, mqtt_port, topic):
    """
    Підключаємо клієнта MQTT для отримання та збереження даних у базу.
    """
    client = mqtt.Client()
    client.on_connect = lambda c, u, f, rc: print(f"Підключено до MQTT брокера з кодом {mqtt.connack_string(rc)}")
    client.on_message = on_message  # Підключаємо обробник

    client.connect(mqtt_broker, mqtt_port)
    client.subscribe(topic)  # Підписуємося на тему

    print("MQTT клієнт працює для прийому повідомлень...")
    client.loop_forever()

# Основний блок виконання
if __name__ == "__main__":
    mqtt_broker = "127.0.0.1"
    mqtt_port = 1883
    topic = "iot/healthcare"

    # Запускаємо прийом даних і збереження в базу
    receive_data_from_mqtt(mqtt_broker, mqtt_port, topic)
