from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Lo que envia el user
#Define que para crear un dispositivo necesito obligatoriamente name y device_type. No pido el id ni la fecha, porque eso lo genera el sistema solo.
class DeviceCreate(BaseModel):
    name: str
    device_type: str
    status: str = "active"

# Lo que responde el sistema. #Define qué le devuelvo al usuario cuando consulta la lista.
# Aquí sí incluyo el id y la last_reading_at para que pueda ver cuándo se actualizó por última vez.
class DeviceResponse(BaseModel):
    id: int
    name: str
    device_type: str
    status: str
    created_at: datetime
    last_reading_at: Optional[datetime] = None

    class Config:
        from_attributes = True