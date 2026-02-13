#La funcion de este archivo es saber donde estan los dato y como acceder a ellos.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1-Esto crea un archivo de base de datos llamado "iot.db". Es donde se van a guardar los datos.
SQLALCHEMY_DATABASE_URL = "sqlite:///./iot.db"

# 2-Configuramos el motor de la base de datos. Es lo que "viaja" entre el codigo y el archivo de datos.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) #El argumento check_same_thread": False deja que vario hilos toquen la conexion.

# 3-Creamos la sesión para guardar/leer datos
# Hace la función como de "carrito" de datos.
# - autocommit=False: No guardes cambios automáticamente, espera a que yo te diga "CONFIRMAR".
# - autoflush=False: No envíes datos a la DB hasta que yo te diga.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4-Esta es la base para nuestros modelos (tablas), está en blanco.
Base = declarative_base()

# 5-Esta función nos ayuda a obtener la base de datos en cada petición.
# Cada vez que entra una petición
#   a. Abre una sesión (db = SessionLocal())
#   b. Te la presta (yield db) para que trabajes.
#   c. Cuando terminas, pase lo que pase, cierra la sesión (db.close()), para que no bloquee. 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()