from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Importamos nuestros propios archivos
from app import models, schemas, database

# Creamos las tablas en la base de datos automáticamente al iniciar
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="IoT Device Manager")

# 1. Endpoint para CREAR un dispositivo (POST /devices).El argumento: `db: Session = Depends(database.get_db) le dice a FastAPI:
# "Antes de ejecutar esta función, llama al 'mayordomo' (get_db),
# dame la sesión que creó, y cuando termine la función, devuélvesela para cerrar".
@app.post("/devices", response_model=schemas.DeviceResponse)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(database.get_db)):
    # Creamos el objeto usando el modelo de la base de datos
    # Paso A: Convertir datos del usuario (Pydantic) a datos de base de datos (SQLAlchemy Model)
    # El usuario manda JSON, pero la DB necesita un objeto Python clase Device
    db_device = models.Device(
        name=device.name, 
        device_type=device.device_type, 
        status=device.status
    )
    # Paso B: "Anotar en el carrito"
    db.add(db_device)     # Lo añadimos a la sesión
    # Paso C: "Confirmar compra"
    db.commit()           # Guardamos cambios
    # Paso D: "Recargar"
    db.refresh(db_device) # Recargamos para obtener el ID generado
    return db_device

# 2. Endpoint para LISTAR dispositivos (GET /devices)
@app.get("/devices", response_model=List[schemas.DeviceResponse])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    devices = db.query(models.Device).offset(skip).limit(limit).all()
    return devices

# 3. Endpoint para obtener UN dispositivo (GET /devices/{id})
@app.get("/devices/{device_id}", response_model=schemas.DeviceResponse)
def read_device(device_id: int, db: Session = Depends(database.get_db)):
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device