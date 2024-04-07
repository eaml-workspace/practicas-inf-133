from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

animales=[
    {
    "id": 1,
    "nombre": "Icca",
    "especie": "Panda",
    "edad": 3,
    "genero":"Hembra",
    "peso":45,
    },
    {
    "id": 2,
    "nombre": "Pedro",
    "especie": "Leano",
    "edad": 50,
    "genero":"Macho",
    "peso":102,
    },
]

class AnimalService:
    @staticmethod
    def add_animal(data):
        data["id"]= len(animales)+1
        animales.append(data)
        return animales
    
    @staticmethod 
    def get_animales():
        return animales
    
    @staticmethod
    def find_animal_especie(especie):
        return next((animal for animal in animales if animal["especie"]== especie),
            None
        )

    @staticmethod
    def find_animal_genero(genero):
        return next(
            (animal for animal in animales if animal["genero"] == genero),
            None,
        )

    @staticmethod
    def update_animal(ci,data):
        animal = AnimalService.find_animal_id(ci)
        if animal:
            animal.update(data)
            return animales
        else:
            return None 
    
    @staticmethod
    def delete_animal(id):
        animal = AnimalService.find_animal_id(id)
        if animal:
            animales.remove(animal)
            return animales
        else:
            return None
    
    @staticmethod
    def find_animal_id(id):
        return next(
            (animal for animal in animales if animal["id"] == id),
            None,
        )

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

class AnimalHandler(BaseHTTPRequestHandler):
    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if self.path.startswith("/animales/"):
            id= int(self.path.split("/")[-1])
            animal = AnimalService.find_animal_id(id)
            if animal:
                HTTPDataHandler.handle_response(self, 200, [animal])
            else:
                HTTPDataHandler.handle_response(self, 204, [])
        
        elif parsed_path.path == "/animales":
            if "especie" in query_params:
                especie = query_params["especie"][0]
                animales_filtrados= AnimalService.find_animal_especie(especie)
                if animales_filtrados != []:
                    HTTPDataHandler.handle_response(self, 200, animales_filtrados)
                else:
                    HTTPDataHandler.handle_response(self, 204, [])
            elif "genero" in query_params:            
                genero = query_params["genero"][0]
                animales_filtrados = AnimalService.find_animal_genero(genero)
                if animales_filtrados != []:
                    HTTPDataHandler.handle_response(self, 200, animales_filtrados)
                else:
                    HTTPDataHandler.handle_response(self, 204, [])
            else:
                HTTPDataHandler.handle_response(self, 200, animales)
            
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error":"Ruta no existente"})
        
    def do_POST(self):
        if self.path == "/animales":
            data = self.read_data()
            animales = AnimalService.add_animal(data)
            HTTPDataHandler.handle_response(self, 201, animales)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error":"Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id= int(self.path.split("/")[-1])
            data= self.read_data()
            animales = AnimalService.update_animal(id, data)
            if animales:
                HTTPDataHandler.handle_response(self, 200, animales)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error":"Animal no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error":"Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith == "/animales/":
            id= int(self.path.split("/")[-1])
            animales = AnimalService.delete_animal(id)
            HTTPDataHandler.handle_response(self, 200, animales)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, AnimalHandler)
        print(f" Dale !!!! Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()