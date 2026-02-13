from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Lo que envia el user
class DeviceCreate(BaseModel):
    name: str
    device_type: str
    status: str = "active"

# Lo que responde el sistema
class DeviceResponse(BaseModel):
    id: int
    name: str
    device_type: str
    status: str
    created_at: datetime
    last_reading_at: Optional[datetime] = None

    class Config:
        from_attributes = True