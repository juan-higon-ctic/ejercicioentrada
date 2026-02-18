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
    """
    global running
    contador_ciclos = 0 
    
    print("\033[94m--- MOTOR DE RECOLECCIÓN INICIADO  ---\033[0m")
    
    while running:
        contador_ciclos += 1
        db: Session = SessionLocal()
        
        try:
            # 1. Obtenemos el punto de partida (cuántas hay ahora)
            total_filas = db.query(func.count(models.Measurement.id)).scalar()
            
            # --- LÓGICA DE AUTO-LIMPIEZA (50 MEDIDAS) ---
            if total_filas >= totalmedidas:
                print(f"\n\033[43m\033[30m [SISTEMA] UMBRAL MÁXIMO ALCANZADO: {total_filas} medidas. \033[0m")
                db.query(models.Measurement).delete()
                db.commit()
                print("\033[92m [SISTEMA] Historial vaciado. \033[0m\n")
                # Si limpiamos, empezamos a contar desde 0
                total_filas = 0 
            # ----------------------------------------------------

            # Variable para ir sumando en este ciclo
            numero_para_esta_medida = total_filas #Tamaño de la base de datos antes de sumarle las medidas nuevas

            devices = db.query(models.Device).filter(models.Device.status == True).all()    
            timestamp = datetime.now()

            print(f"\n\033[95m>>> INICIANDO CICLO DE MEDIDA Nº {contador_ciclos} <<<\033[0m")
            
            for device in devices:
                # 2. TU LÓGICA: Sumamos 1 a cada iteración del dispositivo
                numero_para_esta_medida += 1 #Para darle un numero a cada medida se suma un valor al tamaño de la tabla dependiendo de que medida sea

                reading = {
                    "voltage": round(random.uniform(220.0, 240.0), 2),
                    "current": round(random.uniform(10.0, 15.0), 2),
                    "power": round(random.uniform(2500.0, 3000.0), 2)
                }

                # 3. Creamos el objeto con el contador actualizado
                nueva_medicion = models.Measurement(
                    Measurement=numero_para_esta_medida, # Nombre correcto del campo
                    voltage=reading["voltage"],
                    current=reading["current"],
                    power=reading["power"],
                    device_id=device.id,
                    timestamp=timestamp
                )
                
                db.add(nueva_medicion)
                db.flush() 
                id_real = nueva_medicion.id 
                
                # Imprimimos con ambos números para verificar
                print(f"\033[93m[DB ID #{id_real} | Medida #{numero_para_esta_medida}]\033[0m Dispositivo: {device.name}")

                if reading["voltage"] > umbral:
                    print(f"\033[91m    ¡ALERTA! Voltaje crítico: {reading['voltage']}V\033[0m")
                
                # Actualizar el "tiempo real" del dispositivo
                device.voltage = reading["voltage"]
                device.current = reading["current"]
                device.power = reading["power"]
                device.last_reading_at = timestamp

            # Confirmamos todas las medidas del ciclo
            db.commit()
            
        except Exception as e:
            db.rollback() 
            print(f"\033[41m Error en el proceso de recolección: {e} \033[0m")
        
        finally:
            db.close()
        
        await asyncio.sleep(5) 

    print("\033[94m--- MOTOR DE RECOLECCIÓN DETENIDO ---\033[0m")