from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Device(Base): #Tabla inicial, la que guarda la medidas
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
    measurements = relationship("Measurement", back_populates="device")

class Measurement(Base): #Tabla para guardar el valor maximo
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    voltage = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relación con el dispositivo
    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("Device", back_populates="measurements")