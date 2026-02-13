# 1. Usamos una versión ligera de Python
FROM python:3.11-slim

# 2. Evitamos que Python genere archivos temporales innecesarios
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Creamos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalamos las dependencias primero (para que sea más rápido)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todo el código de nuestro proyecto
COPY . .

# 6. Exponemos el puerto 8000 para poder entrar desde el navegador
EXPOSE 8000

# 7. Comando para arrancar la app automáticamente
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]