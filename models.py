from sqlalchemy import Column, Integer, String, Float
from database import Base

class IoTData(Base):
    __tablename__ = "iot_data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, nullable=False)
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
    temperature_c = Column(Float, nullable=False)  # Температура в градусах Цельсія
    humidity = Column(Float, nullable=False)       # Вологість у відсотках
    
    