from fastapi import APIRouter, Depends, HTTPException, Query # <--- IMPORTANTE: Añadir Query aquí
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database
from app.database import get_db

# Configuramos el router
router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("/", response_model=schemas.DeviceResponse) #funcion para subir un nuevo dispositivo
def create_device(device: schemas.DeviceCreate, db: Session = Depends(database.get_db)):
    """
    Endpoint para registrar un nuevo dispositivo IoT en el sistema.
    """
    # 1. Convertimos los datos que vienen de la web (Pydantic) a un modelo de Base de Datos (SQLAlchemy)
    db_device = models.Device(**device.model_dump())
    
    # 2. Añadimos el objeto a la sesión y guardamos en la base de datos
    db.add(db_device)
    db.commit() # Confirmamos la transacción
    
    # 3. Refrescamos el objeto para obtener los datos generados por la DB (como el ID autoincremental)
    db.refresh(db_device)
    return db_device

@router.get("/", response_model=List[schemas.DeviceResponse]) #funcion para recibir las de la base de datos
def read_devices(db: Session = Depends(database.get_db)):
    """
    Endpoint para obtener el listado completo de dispositivos registrados.
    """
    # Realiza una consulta SELECT * FROM devices y devuelve todos los resultados
    return db.query(models.Device).all()

@router.delete("/{device_id}") #funcion para borrar un dispositivo
def delete_device(device_id: int, db: Session = Depends(database.get_db)):
    """
    Endpoint para eliminar un dispositivo mediante su ID único.
    """
    # 1. Buscamos el dispositivo por su ID en la base de datos
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    
    # 2. Si no existe, lanzamos un error 404 (Not Found)
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    # 3. Si existe, lo borramos y confirmamos la operación
    db.delete(db_device)
    db.commit()
    
    return {"message": "Dispositivo eliminado con éxito"}

@router.patch("/{device_id}/rename") #funcion para cambiar el nombre de algun dispositivo
def rename_device(
    device_id: int, 
    new_name: str = Query(..., description="El nuevo nombre para el dispositivo"),
    db: Session = Depends(get_db)
):
    """
    **Cambiar nombre de dispositivo:**
    Permite actualizar el nombre de un dispositivo existente usando su ID.
    """
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    device.name = new_name
    db.commit()
    db.refresh(device)
    
    return {"status": "ok", "new_name": device.name}