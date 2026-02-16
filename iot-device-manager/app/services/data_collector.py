import asyncio
import random
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

# Variable global que actúa como interruptor (ON/OFF)
# Se cambia desde los endpoints de la API en collector.py
running = False

async def collect_data():
    """
    Función asíncrona que ejecuta el bucle de recolección.
    Se ejecuta en segundo plano sin bloquear el resto de la API.
    """
    global running
    print("--- INICIANDO MOTOR DE RECOLECCIÓN DE DATOS ---")
    
    while running:
        # 1. Creamos una sesión local con la base de datos
        # Se abre y cierra en cada iteración para evitar fugas de memoria
        db: Session = SessionLocal()
        
        try:
            # 2. Consultamos la DB para obtener solo dispositivos con status 'active'
            # Si un dispositivo está 'inactive', el recolector lo ignorará automáticamente
            devices = db.query(models.Device).filter(models.Device.status == "active").all()
            
            # Obtenemos la hora actual para aplicarla a todas las lecturas de esta vuelta
            timestamp = datetime.now()
            
            for device in devices:

                reading = {
                    "voltage": round(random.uniform(220.0, 240.0), 2),
                    "current": round(random.uniform(10.0, 15.0), 2),
                    "power": round(random.uniform(2500.0, 3000.0), 2)
                }
                print(str(reading))

                # 1. Metemeos los datos en la tabla nueva, la que usaremos como historico
                nueva_medicion = models.Measurement(
                    voltage=reading["voltage"],
                    device_id=device.id,   # Lo vinculamos al ID del dispositivo
                    timestamp=timestamp    # Usamos la hora actual
                )
                
                # 2. Le decimos a la sesión que lo añada
                db.add(nueva_medicion)
                
                device.voltage = reading["voltage"]
                device.current = reading["current"]
                device.power = reading["power"]
                

                # 4. Actualizamos el tiempo 
                device.last_reading_at = timestamp
            
            # 5. Confirmamos los cambios en la base de datos (Guardar)
            db.commit()
            
        except Exception as e:
            # Si algo falla (ej. error de conexión), lo capturamos para que el programa no explote
            print(f"Error en el proceso de recolección: {e}")
        
        finally:
            # 6. Cerramos la sesión de la base de datos SIEMPRE, haya error o no
            db.close()
        
        # 7. Pausa asíncrona de 5 segundos
        # Permite que el procesador atienda otras peticiones mientras espera
        await asyncio.sleep(5) 

    # Mensaje que se verá en consola cuando pongas el estado en False
    print("--- MOTOR DE RECOLECCIÓN DETENIDO ---")