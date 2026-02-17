from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import desc
from app import models, schemas, database
from app.database import get_db

# 1. Configuración del Router
router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("/max-voltage", summary="Obtener el récord de voltaje")
def get_max_voltage(db: Session = Depends(get_db)):
    """
    Busca en el historial el voltaje más alto registrado y 
    nos devuelve el valor, el ID y el nombre del dispositivo.
    """
    # Realizamos un JOIN entre Measurements y Devices para sacar el nombre
    record = db.query(models.Measurement)\
               .join(models.Device)\
               .order_by(desc(models.Measurement.voltage))\
               .first()

    if not record:
        raise HTTPException(status_code=404, detail="No hay lecturas registradas en la base de datos")

    return {
        "max_voltage": record.voltage,
        "device_id": record.device_id,
        "device_name": record.device.name,
        "at_time": record.timestamp
    }

# --- RUTAS GENERALES ---

@router.get("/", response_model=List[schemas.DeviceResponse])
def read_devices(db: Session = Depends(get_db)):
    """Obtener el listado completo de dispositivos."""
    return db.query(models.Device).all()

@router.post("/", response_model=schemas.DeviceResponse)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo dispositivo IoT."""
    db_device = models.Device(**device.model_dump())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

# --- RUTAS CON ID  ---

@router.delete("/{device_id}")
def delete_device(
    device_id: int = Path(..., description="ID del dispositivo a eliminar"), 
    db: Session = Depends(get_db)
):
    """Eliminar un dispositivo por su ID único."""
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    db.delete(db_device)
    db.commit()
    return {"message": "Dispositivo eliminado con éxito"}

@router.patch("/{device_id}/rename")
def rename_device(
    device_id: int, 
    new_name: str = Query(..., description="El nuevo nombre para el dispositivo"),
    db: Session = Depends(get_db)
):
    """Actualizar el nombre de un dispositivo existente."""
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    device.name = new_name
    db.commit()
    db.refresh(device)
    return {"status": "ok", "new_name": device.name}

@router.delete("/history/clear")
def clear_history(
    confirm: bool = Query(..., description="Debes confirmar con 'true' para borrar todo"),
    db: Session = Depends(get_db)
):
    """
    PELIGRO: Borra todos los registros de la tabla de históricos (measurements).
    No borra los dispositivos, solo sus lecturas pasadas.
    """
    if not confirm:
        raise HTTPException(status_code=400, detail="Confirmación requerida")

    try:
        # Borramos todas las filas de la tabla Measurement
        num_rows = db.query(models.Measurement).delete()
        db.commit()
        
        return {
            "message": "Historial eliminado correctamente",
            "filas_borradas": num_rows
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al borrar: {str(e)}")