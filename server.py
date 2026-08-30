import json
from wsgiref.simple_server import make_server

tasks_db = {
    1: {"id": 1, "title": "Aprender WSGI", "done": False}
}
next_id = 2

def application(environ, start_response):
    global tasks_db, next_id
    
    method = environ.get('REQUEST_METHOD', 'GET')
    path = environ.get('PATH_INFO', '')
    
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0
        
    request_body = environ['wsgi.input'].read(request_body_size) if request_body_size > 0 else b""

    headers = [('Content-Type', 'application/json')]

    if method == 'GET' and path == '/tasks':
        status = '200 OK'
        response_data = list(tasks_db.values())

    elif method == 'GET' and path.startswith('/tasks/'):
        id_str = path.split('/')[-1]
        try:
            task_id = int(id_str)
            if task_id in tasks_db:
                status = '200 OK'
                response_data = tasks_db[task_id]
            else:
                status = '404 Not Found'
                response_data = {"error": f"La tarea con id {task_id} no existe"}
        except ValueError:
            status = '404 Not Found'
            response_data = {"error": "El ID debe ser un número entero"}

    elif method == 'POST' and path == '/tasks':
        try:
            new_task_data = json.loads(request_body.decode('utf-8'))
            new_task_data['id'] = next_id
            
            if 'done' not in new_task_data:
                new_task_data['done'] = False
                
            tasks_db[next_id] = new_task_data
            status = '201 Created'
            response_data = new_task_data
            next_id += 1
        except json.JSONDecodeError:
            status = '400 Bad Request'
            response_data = {"error": "El cuerpo de la petición debe ser un JSON válido"}

    elif method == 'PATCH' and path.startswith('/tasks/'):
        id_str = path.split('/')[-1]
        try:
            task_id = int(id_str)
            if task_id in tasks_db:
                patch_data = json.loads(request_body.decode('utf-8'))
                tasks_db[task_id].update(patch_data)
                tasks_db[task_id]['id'] = task_id
                status = '200 OK'
                response_data = tasks_db[task_id]
            else:
                status = '404 Not Found'
                response_data = {"error": f"La tarea con id {task_id} no existe"}
        except ValueError:
            status = '404 Not Found'
            response_data = {"error": "El ID debe ser un número entero"}
        except json.JSONDecodeError:
            status = '400 Bad Request'
            response_data = {"error": "El cuerpo de la petición debe ser un JSON válido"}

    elif method == 'DELETE' and path.startswith('/tasks/'):
        id_str = path.split('/')[-1]
        try:
            task_id = int(id_str)
            if task_id in tasks_db:
                del tasks_db[task_id]
                status = '200 OK'
                response_data = {"message": f"Tarea {task_id} eliminada correctamente"}
            else:
                status = '404 Not Found'
                response_data = {"error": f"La tarea con id {task_id} no existe"}
        except ValueError:
            status = '404 Not Found'
            response_data = {"error": "El ID debe ser un número entero"}

    else:
        status = '404 Not Found'
        response_data = {"error": "Ruta no encontrada o método no permitido"}

    start_response(status, headers)
    return [json.dumps(response_data).encode('utf-8')]

if __name__ == '__main__':
    port = 9292
    with make_server('', port, application) as httpd:
        print(f"Servidor HTTP escuchando en http://localhost:{port}...")
        httpd.serve_forever()