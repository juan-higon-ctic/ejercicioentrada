import asyncio
import random
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

# Variable global para controlar si el job debe seguir corriendo
running = False

async def collect_data():
    """Esta es la función que se ejecutará en bucle infinito."""
    global running
    print("--- Data Collection Job STARTED ---")
    
    while running:
        # 1. Abrimos una sesión de base de datos dedicada para esta vuelta
        # Es importante crear una nueva sesión en cada iteración para no bloquear
        db: Session = SessionLocal()
        
        try:
            # 2. Buscar solo dispositivos 'active'
            devices = db.query(models.Device).filter(models.Device.status == "active").all()
            
            timestamp = datetime.now()
            
            for device in devices:
                # 3. Simular lectura de datos (formato pedido por el PDF)
                print(f"[{timestamp}] Collecting data from device:")
                print(f"({device.device_type}) Mock {device.name} reading:")
                
                # Datos falsos aleatorios
                reading = {
                    "voltage": round(random.uniform(220.0, 240.0), 2),
                    "current": round(random.uniform(10.0, 15.0), 2),
                    "power": round(random.uniform(2500.0, 3000.0), 2)
                }
                print(str(reading))
                
                # 4. Actualizar el timestamp en la base de datos
                device.last_reading_at = timestamp
            
            # Guardar cambios de todos los dispositivos actualizados
            db.commit()
            
        except Exception as e:
            print(f"Error in collection job: {e}")
        finally:
            db.close() # ¡Muy importante cerrar la sesión siempre!
        
        # 5. Esperar X segundos antes de la siguiente vuelta (Intervalo)
        await asyncio.sleep(5) 

    print("--- Data Collection Job STOPPED ---")