from wsgiref.simple_server import make_server
import json

def app(environ, start_response):
    metodo = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]

    if metodo == "POST" and path == "/sumar":
        length = int(environ.get("CONTENT_LENGTH", 0))
        body = environ["wsgi.input"].read(length)
        data = json.loads(body)

        resultado = data["a"] + data["b"]

        respuesta = {"suma": resultado}

        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(respuesta).encode("utf-8")]

    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Ruta no encontrada"]

server = make_server("localhost", 8000, app)
print("Servidor WSGI en http://localhost:8000")
server.serve_forever()