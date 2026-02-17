from fastapi import APIRouter
import asyncio
from app.services import data_collector

# Configuramos el enrutador con un prefijo para que todas las rutas empiecen por /collector
# El parámetro 'tags' ayuda a organizar la documentación en Swagger
router = APIRouter(prefix="/collector", tags=["Collector Control"])

@router.post("/start")
async def start_worker():
    """
    Endpoint para activar la recolección de datos.
    """
    # 1. Verificamos si el motor ya está encendido para evitar duplicar procesos
    if data_collector.running:
        return {"status": "El recolector ya está funcionando"}
    
    # 2. Cambiamos la variable global a True para permitir que el bucle se ejecute
    data_collector.running = True
    
    # 3. 'asyncio.create_task' dispara la función en segundo plano.
    # Esto permite que la API responda "OK" de inmediato al usuario 
    # mientras el motor sigue trabajando por su cuenta en la terminal.
    asyncio.create_task(data_collector.collect_data())
    
    return {"status": "Recolector iniciado"} #informamos al usuario de que funciona 

@router.post("/stop")
async def stop_worker():
    """
    Endpoint para detener la recolección de datos.
    """
    # Simplemente cambiamos el interruptor a False. 
    # La próxima vez que el bucle del motor termine su pausa de 5 segundos,
    # verá que running es False y se detendrá solo.
    data_collector.running = False
    
    return {"status": "Se ha enviado la señal de parada"}