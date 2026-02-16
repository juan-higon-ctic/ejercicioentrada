from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from app.database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True) #el id de cada elemento
    name = Column(String, index=True) #el nombre de cada elemento
    device_type = Column(String)  # Ej: "sensor_temperatura"
    status = Column(String, default="active")  # Ej: "active", "inactive"
    created_at = Column(DateTime, default=datetime.utcnow)
    # Este campo puede estar vacío (nullable) al principio
    last_reading_at = Column(DateTime, nullable=True)
    #valores de lectura de los sensores
    voltage = Column(Float, nullable=True) 
    current = Column(Float, nullable=True)
    power = Column(Float, nullable=True)