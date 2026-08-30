# practica-de-verbos-Adriel-Palacio

GET: Se usa solamente para consultar informacion, y no altera los datos en el servidor

POST: Se usa para registrar o crear un nuevo recurso en el servidor

PATCH: Se usa para modificar solamente ciertos campos de un recurso sin sobrescribir el objeto entero

DELETE: Se usa para borrar un recurso con su id

(POST no es idempotente porque si ejecutas la misma orden POST tres veces seguidas, el servidor no va a conservar el estado original: va a crear tres tareas independientes en la memoria)
