from wsgiref.simple_server import make_server
import json

libros = []
contador_id = 1

def app(environ, start_response):
    global contador_id

    metodo = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]

    if metodo == "GET" and path == "/libros":
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(libros).encode("utf-8")]

    if metodo == "POST" and path == "/libros":
        length = int(environ.get("CONTENT_LENGTH", 0))
        body = environ["wsgi.input"].read(length)
        if not body:
                start_response("400 Bad Request", [("Content-Type", "text/plain")])
                return [b"Body vacio"]
        data = json.loads(body)

        libro = {
            "id": contador_id,
            "titulo": data["titulo"],
            "autor": data["autor"],
            "anio": data["anio"]
        }

        libros.append(libro)
        contador_id += 1

        start_response("201 Created", [("Content-Type", "application/json")])
        return [json.dumps(libro).encode("utf-8")]

    if metodo == "GET" and path.startswith("/libros/"):
        try:
            libro_id = int(path.split("/")[-1])
        except ValueError:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"No encontrado"]

        for libro in libros:
            if libro["id"] == libro_id:
                start_response("200 OK", [("Content-Type", "application/json")])
                return [json.dumps(libro).encode("utf-8")]

        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"Libro no encontrado"]

    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Ruta no encontrada"]

server = make_server("localhost", 8000, app)
print("Servidor WSGI en http://localhost:8000")
server.serve_forever()