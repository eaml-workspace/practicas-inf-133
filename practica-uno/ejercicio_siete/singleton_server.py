from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
import random

partidas={}

class IDs:
    def id_partida():
        llaves= list(partidas.keys())
        llaves.sort()
        if llaves == []:
            llaves.append(1)
            return llaves[-1]
        else:
            a=llaves[-1]+1
            llaves.append(a)
            return a

class Partida:
    _instance= None
    
    def __new__(cls, elemento):
        elemento_server= random.choice(['piedra', 'tijera', 'papel'])
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.elemento = elemento
            cls._instance.elemento_server = elemento_server
        return cls._instance
    
    def to_dict(self):
        return {"jugador": self.elemento, "maquina": self.elemento_server, "resultado": Partida.resultado}
    
    def resultado(self):
        a=(self.elemento , self.elemento_server)
        gano=[("piedra","tijera"),("papel","piedra"),("tijera","papel")]
        if self.elemento == self.elemento_server:
            return "empate"
        elif a in gano:
            return "ganó"
        else:
            return "perdió"
    
    def partidas_get(self):
        partida_get = self.to_dict()
        a=IDs.id_partida()
        partidas[a] = partida_get
        return partidas
    
class HTTPDataHandler(BaseHTTPRequestHandler):
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

class PartidaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if self.path == "/partidas":
            HTTPDataHandler.handle_response(self, 200, partidas)
        ##elif query_params
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
    
    def do_POST(self):
        if self.path == "/partidas/elemento":
            content_length = self.headers["Content-Length"]
            post_data = str(self.rfile.read(content_length))
            elemento = json.loads(post_data.decode("utf-8"))["elemento"]
            partida.resultado(elemento)
            partida_data =partida.to_dict()
            HTTPDataHandler.handle_response(self, 200, partida_data)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

def main():
    global partida
    partida = Partida(PartidaHandler.do_POST)

    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, PartidaHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()