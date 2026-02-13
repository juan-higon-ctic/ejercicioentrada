from fastapi import APIRouter
import asyncio
from app.services import data_collector

router = APIRouter(prefix="/collector", tags=["Collector Control"])

@router.post("/start")
async def start_worker():
    if data_collector.running:
        return {"status": "El recolector ya está funcionando"}
    
    data_collector.running = True
    # Iniciamos la tarea en segundo plano
    asyncio.create_task(data_collector.collect_data())
    return {"status": "Recolector iniciado"}

@router.post("/stop")
async def stop_worker():
    data_collector.running = False
    return {"status": "Se ha enviado la señal de parada"}