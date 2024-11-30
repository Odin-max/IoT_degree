from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from save_to_postgres import IoTAnalysis

# Підключення до PostgreSQL
DATABASE_URL = "postgresql://postgres:PG13@localhost/iot_analysis_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def fetch_data():
    """
    Отримує всі записи з бази даних PostgreSQL.
    """
    entries = session.query(IoTAnalysis).all()
    for entry in entries:
        print(f"Device ID: {entry.device_id}, Data Rate: {entry.data_rate_kbps}, Anomaly: {entry.anomaly}, Timestamp: {entry.timestamp}")

if __name__ == "__main__":
    fetch_data()
