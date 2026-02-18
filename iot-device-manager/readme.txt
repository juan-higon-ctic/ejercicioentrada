1. requirements.txt 
Es el primer archivo que usas. Contiene la lista de "herramientas" (librerías) que Python necesita instalar (FastAPI, SQLAlchemy, etc.) 
para que el proyecto pueda existir. Sin esto, nada arrancaría.

2. database.py 
Este es el siguiente en activarse. Configura la conexión con el archivo iot.db.
Crea el motor de comunicación y la "sesión", que es el canal por el que viajarán los datos desde Python hasta el disco duro.

3. models.py
Define cómo es la "ficha" de un dispositivo en la base de datos (nombre, tipo, estado). 
Es el traductor que le dice a SQLite: "Crea una tabla con estas columnas". Se usa al principio para crear la estructura de la base de datos.

4. schemas.py 
Antes de que un dato entre a la API, pasa por aquí. 
Define qué campos son obligatorios cuando un usuario envía datos (ej. el nombre no puede estar vacío). Es el filtro que asegura que nadie envíe información basura o mal escrita.

5. main.py 
Es el punto de entrada. Cuando ejecutas el servidor, este archivo:
-Llama a models.py para asegurarse de que las tablas estén creadas.
-Importa todas las rutas (endpoints) de la carpeta api.
-Arranca la aplicación FastAPI y se queda esperando peticiones.

6. app/api/devices.py 
-Cuando tú quieres crear un dispositivo desde el navegador, este archivo entra en acción. Recibe tu petición, valida los datos con los schemas y le pide a la database que guarde el nuevo dispositivo.

7. app/api/collector.py 
-Este documento solo tiene una misión: gestionar el botón de encendido y apagado del sistema de recolección. No recolecta datos por sí mismo, solo le da la orden al "empleado" que está en la carpeta de servicios.

8. app/services/data_collector.py  Este es el archivo que más trabaja. Se activa solo cuando collector.py le da la orden.
-Entra en un bucle infinito.
-Mira la base de datos.
-Genera números aleatorios (voltaje, corriente).
-Escribe en la terminal y actualiza los registros.

9. Dockerfile y docker-compose.yml 
Se usan al final, cuando el código ya funciona. Sirven para "empaquetar" todo lo anterior en un contenedor.
Así, el profesor puede ejecutar tu proyecto en su ordenador sin tener que configurar nada, garantizando que funcione exactamente igual que en el tuyo.

----------------------------------------------------------------------------------------------------------------------------------------------
Verbos
Devices
GET /devices/max-voltage --Imprime por consola el valor maximo y el nombre del dispotivo que lo midió
GET /devices/ --Imprime los datos de todos los dispositivos
POST /devices/ --Añade un dispositivo
DELETE /devices/{devices_id} --Borra un dispositivo, hay que concretar su id 
PATCH /devices/{devices_id} --Cambia el nombre de un dispositivo, hay que concreta su id
DELETE /devices/history/clear --Borra toda la base de datos. SE ACTIVA AUTOMATICAMENTE CUANDO EL NUMERO DE MEDIAS SUPERA UN UMBRAL ESTABLECIDO, POR DEFECTO 50.
PUT /devices/{devices_id}/status --Cambia el status de un dispositivo

Collector Control
/collector/start--Inicia el proceso de recoleccion de Datos
/collector/stop--Termina la recoleccion,

Por consola se iprimen los valores de voltage,current y power de cada dispotivo siguiendo el formato de lo siguientes mensajes:

iot-app-1  | >>> INICIANDO CICLO DE MEDIDA Nº 279 <<<
iot-app-1  |  Medida dispositivo Dispositivo 1                                                                                                                                               
iot-app-1  | {'voltage': 231.92, 'current': 10.55, 'power': 2794.18}                                                                                                                         
iot-app-1  |  ¡ALERTA! El voltaje de Dispositivo 1  es 231.92V (Mayor de 230)
iot-app-1  |  Medida dispositivo Dispositivo 2                                                                                                                                               
iot-app-1  | {'voltage': 233.06, 'current': 10.32, 'power': 2981.75}                                                                                                                         
iot-app-1  |  ¡ALERTA! El voltaje de Dispositivo 2 es 233.06V (Mayor de 230)                                                                                                                 
iot-app-1  |  Medida dispositivo Dispositivo 3
iot-app-1  | {'voltage': 237.2, 'current': 13.69, 'power': 2705.82}                                                                                                                          
iot-app-1  |  ¡ALERTA! El voltaje de Dispositivo 3 es 237.2V (Mayor de 230)                                                                                                                  
iot-app-1  |  Medida dispositivo string
iot-app-1  | {'voltage': 232.65, 'current': 14.98, 'power': 2815.84}                                                                                                                         
iot-app-1  |  ¡ALERTA! El voltaje de string es 232.65V (Mayor de 230)                                                                                                                        

Como se puede ver hay una alerta para cuando el valor de voltage es superior a un threshold de 230.                                                        
-----------------------------------------------------------------------------------------------------------------------------------------------
FASTAPI URL
http://127.0.0.1:8000/docs#/

Grafana URL
http://127.0.0.1:3000/

-----------------------------------------------------------------------------------------------------------------------------------------------
Bases de datos

iot.db Contiene dos tablas relacionadas por el id del dispositivo, una sirve para obtener los datos de la ultima medida, la otra para guardar los valores historicos, se utitiliza
para obtener el valor maximo de los voltios cuando se usa el comando GET /devices/max-voltage. 
