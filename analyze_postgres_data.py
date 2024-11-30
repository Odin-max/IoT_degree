from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from save_to_postgres import IoTData  # Підключення моделі IoTData

# Налаштування бази даних
DATABASE_URL = "postgresql://postgres:PG13@localhost/iot_analysis_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def analyze_data():
    # Загальна кількість записів
    total_records = session.query(IoTData).count()
    print(f"Загальна кількість записів: {total_records}")

    # Кількість записів за протоколами
    protocol_counts = session.query(IoTData.protocol, func.count(IoTData.id)).group_by(IoTData.protocol).all()
    print("\nКількість записів за протоколами:")
    for protocol, count in protocol_counts:
        print(f"  {protocol}: {count}")

    # Пристрої з найбільшою кількістю аномалій
    anomaly_devices = (
        session.query(IoTData.device_id, func.count(IoTData.anomaly))
        .filter(IoTData.anomaly != "None")
        .group_by(IoTData.device_id)
        .order_by(func.count(IoTData.anomaly).desc())
        .limit(5)
        .all()
    )
    print("\nПристрої з найбільшою кількістю аномалій:")
    for device, count in anomaly_devices:
        print(f"  {device}: {count}")

    # Середній рівень передачі даних (kbps) за протоколами
    avg_data_rate = session.query(IoTData.protocol, func.avg(IoTData.data_rate_kbps)).group_by(IoTData.protocol).all()
    print("\nСередній рівень передачі даних (kbps) за протоколами:")
    for protocol, avg_rate in avg_data_rate:
        print(f"  {protocol}: {avg_rate:.2f}")

if __name__ == "__main__":
    analyze_data()
