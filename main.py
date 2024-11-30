from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from database import SessionLocal
from save_to_postgres import IoTData


# poetry run uvicorn main:app --reload


app = FastAPI()

# Налаштування бази даних
DATABASE_URL = "postgresql://postgres:PG13@localhost/iot_analysis_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to the IoT Analysis API!"}

@app.get("/total_records")
def get_total_records():
    total_records = session.query(IoTData).count()
    return {"total_records": total_records}

@app.get("/protocol_distribution")
def get_protocol_distribution():
    protocol_counts = session.query(IoTData.protocol, func.count(IoTData.id)).group_by(IoTData.protocol).all()
    return [{"protocol": protocol, "count": count} for protocol, count in protocol_counts]

@app.get("/top_anomaly_devices")
def get_top_anomaly_devices():
    anomaly_devices = (
        session.query(IoTData.device_id, func.count(IoTData.anomaly))
        .filter(IoTData.anomaly != "None")
        .group_by(IoTData.device_id)
        .order_by(func.count(IoTData.anomaly).desc())
        .limit(5)
        .all()
    )
    return [{"device_id": device, "anomaly_count": count} for device, count in anomaly_devices]

@app.get("/avg_data_rate")
def get_avg_data_rate():
    avg_data_rate = session.query(IoTData.protocol, func.avg(IoTData.data_rate_kbps)).group_by(IoTData.protocol).all()
    return [{"protocol": protocol, "avg_data_rate_kbps": avg_rate} for protocol, avg_rate in avg_data_rate]


@app.get("/iot-data")
def get_iot_data(db: Session = Depends(get_db)):
    """
    Ендпоінт для отримання даних IoT з бази.
    Параметри:
        - skip: кількість записів, які потрібно пропустити (для пагінації)
        - limit: максимальна кількість записів
    """
    data = db.query(IoTData).all()
    if not data:
        raise HTTPException(status_code=404, detail="Дані не знайдено")
    return {"iot_data": data}