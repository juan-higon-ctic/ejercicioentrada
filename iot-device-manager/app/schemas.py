from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Lo que envia el user
#Define que para crear un dispositivo necesito obligatoriamente name y device_type. No pido el id ni la fecha, porque eso lo genera el sistema solo.
class DeviceCreate(BaseModel):
    name: str
    device_type: str
    status: str = "active"

class DeviceUpdateName(BaseModel): #funcion para cmambiar el nombre
    name: str

# Lo que responde el sistema. #Define qué le devuelvo al usuario cuando consulta la lista.
# Aquí sí incluyo el id y la last_reading_at para que pueda ver cuándo se actualizó por última vez.
class DeviceResponse(BaseModel):
    id: int
    name: str
    device_type: str
    status: str
    created_at: datetime
    last_reading_at: Optional[datetime] = None
    voltage: Optional[float] = None
    current: Optional[float] = None
    power: Optional[float] = None

    class Config:
        from_attributes = True


# Esquema base con los datos comunes
class MeasurementBase(BaseModel):
    voltage: float
    device_id: int

# Esquema para las respuestas de la API 
class MeasurementResponse(MeasurementBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True # Esto permite leer modelos de SQLAlchemy