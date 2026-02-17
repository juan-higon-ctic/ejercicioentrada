import asyncio
import random
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from sqlalchemy import func  # Importamos func para contar las filas

#Variables
totalmedidas=50 #Numero maximo de medidas que puede guardar la tabla de la base de datos
umbral=230 #Valor a partir del cual se alerta de voltage alto


# Variable global que actúa como interruptor (ON/OFF)
running = False

async def collect_data():
    """
    Función asíncrona que ejecuta el bucle de recolección.
    Incluye auto-limpieza al superar las 50 medidas.
    """
    global running
    # Contador de ciclos de esta sesión
    contador_ciclos = 0 
    
    print("\033[94m--- MOTOR DE RECOLECCIÓN INICIADO  ---\033[0m")
    
    while running:
        contador_ciclos += 1
        db: Session = SessionLocal()
        
        try:
            # --- MEJORA: LÓGICA DE AUTO-LIMPIEZA (50 MEDIDAS) ---
            # Contamos cuántas filas hay actualmente en la tabla de históricos
            total_filas = db.query(func.count(models.Measurement.id)).scalar()
            
            if total_filas >= totalmedidas:
                print(f"\n\033[43m\033[30m [SISTEMA] UMBRAL MÁXIMO ALCANZADO: {total_filas} medidas. \033[0m")
                print("\033[33m Ejecutando limpieza automática del historial... \033[0m")
                
                # Borramos todos los registros de la tabla Measurement
                db.query(models.Measurement).delete()
                db.commit()
                
                print("\033[92m [SISTEMA] Historial vaciado. Reiniciando almacenamiento. \033[0m\n")
            # ----------------------------------------------------

            # Consultamos dispositivos activos
            devices = db.query(models.Device).filter(models.Device.status == "active").all()
            timestamp = datetime.now()

            print(f"\n\033[95m>>> INICIANDO CICLO DE MEDIDA Nº {contador_ciclos} <<<\033[0m")
            
            for device in devices:
                # Generamos los valores aleatorios
                reading = {
                    "voltage": round(random.uniform(220.0, 240.0), 2),
                    "current": round(random.uniform(10.0, 15.0), 2),
                    "power": round(random.uniform(2500.0, 3000.0), 2)
                }

                # Creamos el objeto de medición para el histórico
                nueva_medicion = models.Measurement(
                    voltage=reading["voltage"],
                    device_id=device.id,
                    timestamp=timestamp
                )
                
                db.add(nueva_medicion)
                db.flush() # Obtenemos el ID real antes del commit
                id_real = nueva_medicion.id 
                
                # Imprimimos los datos con el ID real
                print(f"\033[93m[Registro DB #{id_real}]\033[0m Medida dispositivo: {device.name}")
                print(f"    Valores: {reading}")

                # Alerta de sobrevoltaje
                if reading["voltage"] > umbral:
                    print(f"\033[91m    ¡ALERTA! Voltaje crítico en registro #{id_real}: {reading['voltage']}V\033[0m")
                
                # Actualizamos el estado actual en la tabla de dispositivos
                device.voltage = reading["voltage"]
                device.current = reading["current"]
                device.power = reading["power"]
                device.last_reading_at = timestamp

            # Confirmamos todos los cambios
            db.commit()
            
        except Exception as e:
            db.rollback() 
            print(f"\033[41m Error en el proceso de recolección: {e} \033[0m")
        
        finally:
            db.close()
        
        # Pausa de 5 segundos
        await asyncio.sleep(5) 

    print("\033[94m--- MOTOR DE RECOLECCIÓN DETENIDO ---\033[0m")