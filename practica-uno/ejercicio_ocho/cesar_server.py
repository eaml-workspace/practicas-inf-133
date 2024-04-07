from http.server import HTTPServer, BaseHTTPRequestHandler
import json

mensajes= {}

class IDs:
    def id_mensaje():
        llaves= list(mensajes.keys())
        llaves.sort()
        if llaves == []:
            llaves.append(1)
            return llaves[-1]
        else:
            a=llaves[-1]+1
            llaves.append(a)
            return a

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

class MensajeService:
    @staticmethod
    def add_mensaje(data):
        id=IDs.id_mensaje()
        mensajes[id]=data
        return mensajes
    
    @staticmethod
    def update_mensajes(data,id):
        for index, mensaje in mensajes.items():
            if index==id:
                mensaje=data
        return mensajes

    @staticmethod
    def mensaje_id(id):
        return {index: mensaje for index, mensaje in mensajes if index==id}
    
    @staticmethod
    def delete_mensaje(id):
        if id in mensajes:
            return mensajes.pop(id)
        else:
            return None

class MensajeHandler(BaseHTTPRequestHandler):
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
    
    def do_POST(self):
        if self.path == "/mensajes":
            data = self.read_data()
            mensaje = MensajeService.add_mensaje(data)
            HTTPDataHandler.handle_response(self, 201, mensaje)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error":"Ruta no existente"})
    
    def do_GET(self):
        if self.path == "/mensajes":
            HTTPDataHandler.handle_response(self, 200, mensajes)
            
        elif self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            mensaje = MensajeService.mensaje_id(id)
            if mensaje:
                HTTPDataHandler.handle_response(self, 200, mensaje)
            else:
                HTTPDataHandler.handle_response(self, 204, [])
            
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error":"Ruta no existente"})
    
    def do_PUT(self):
        if self.path.startswith("/mensajes/"):
            id= int(self.path.split("/")[-1])
            data= self.read_data()
            mensaje = MensajeService.update_mensajes(id, data)
            if mensaje:
                HTTPDataHandler.handle_response(self, 200, mensaje)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error":"Mensaje no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error":"Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith == "/mensajes/":
            id= int(self.path.split("/")[-1])
            mensaje = MensajeService.delete_mensaje(id)
            HTTPDataHandler.handle_response(self, 200, mensaje)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, MensajeHandler)
        print(f" Dale !!!! Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()