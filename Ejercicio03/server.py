from wsgiref.simple_server import make_server
import json, os, mimetypes
from urllib.parse import unquote

STATIC_DIR = "static"

def servir_estatico(path):
    file_path = path.lstrip("/")
    full_path = os.path.join(STATIC_DIR, file_path.replace("static/", ""))

    if not os.path.isfile(full_path):
        return None, None

    content_type, _ = mimetypes.guess_type(full_path)
    if content_type is None:
        content_type = "application/octet-stream"

    with open(full_path, "rb") as f:
        return f.read(), content_type

def app(environ, start_response):
    metodo = environ["REQUEST_METHOD"]
    path = unquote(environ["PATH_INFO"])

    if metodo == "GET" and path == "/":
        contenido, tipo = servir_estatico("/static/index.html")
        start_response("200 OK", [("Content-Type", tipo)])
        return [contenido]

    if metodo == "GET" and path == "/saludo":
        data = {"msg": "Hola"}
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(data).encode("utf-8")]

    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Ruta no encontrada"]

server = make_server("localhost", 8000, app)
print("Servidor WSGI en http://localhost:8000")
server.serve_forever()