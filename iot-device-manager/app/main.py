from fastapi import FastAPI
from app import models, database
from app.api import devices, collector

# 1. Crear las tablas de la base de datos automáticamente al arrancar
# Esto lee los modelos de models.py y crea el archivo iot.db si no existe
models.Base.metadata.create_all(bind=database.engine)

# 2. Inicializar la aplicación FastAPI
app = FastAPI(
    title="Prueba IoT Device Management System",
    description="API para gestionar dispositivos IoT y simular recolección de datos",
)

# 3. Incluir las rutas (Endpoints) de nuestros archivos en la carpeta api/
# 'devices.router' contiene las rutas para crear/listar dispositivos
app.include_router(devices.router)

# 'collector.router' contiene las rutas para iniciar/parar la recolección
app.include_router(collector.router)

# 4. Ruta base de cortesía
@app.get("/", tags=["General"])
def read_root():
    return {
        "message": "Bienvenido a la API de Gestión IoT",
        "docs": "Ve a /docs para ver la documentación interactiva",
        "status": "online"
    }

# Si quieres que el servidor se detenga limpiamente, puedes añadir eventos aquí
@app.on_event("shutdown")
def shutdown_event():
    print("Apagando el sistema de gestión IoT...")