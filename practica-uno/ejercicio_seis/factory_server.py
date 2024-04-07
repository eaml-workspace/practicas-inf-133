from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

animales = {}

class IDs:
    def id_animal():
        llaves= list(animales.keys())
        llaves.sort()
        if llaves == []:
            llaves.append(1)
            return llaves[-1]
        else:
            a=llaves[-1]+1
            llaves.append(a)
            return a

class Zoo:
    def __init__(self, tipo_animal,nombre, especie, genero, edad, peso):
        self.tipo_animal=tipo_animal
        self.nombre =nombre
        self.especie =especie
        self.genero =genero
        self.edad =edad
        self.peso =peso

class Mamifero(Zoo):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("mamifero", nombre, especie, genero, edad, peso)

class Ave(Zoo):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("ave", nombre, especie, genero, edad, peso)

class Reptil(Zoo):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("reptil", nombre, especie, genero, edad, peso)

class Anfibio(Zoo):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("anfibio", nombre, especie, genero, edad, peso)

class Pez(Zoo):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("pez", nombre, especie, genero, edad, peso)

class ZooFactory:
    @staticmethod
    def create_animal(tipo_animal,nombre, especie, genero, edad, peso):
        if tipo_animal=="mamifero":
            return Mamifero(nombre, especie, genero, edad, peso)
        elif tipo_animal == "anfibio":
            return Anfibio(nombre, especie, genero, edad, peso)
        elif tipo_animal == "ave":
            return Ave(nombre, especie, genero, edad, peso)
        elif tipo_animal == "reptil":
            return Reptil(nombre, especie, genero, edad, peso)
        elif tipo_animal == "pez":
            return Pez(nombre, especie, genero, edad, peso)
        else:
            raise ValueError("Tipo de animal no válido")

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

class ZooService:
    def __init__(self):
        self.factory = ZooFactory
    
    def add_animal(self, data):
        tipo_animal = data.get("tipo_animal", None)
        nombre = data.get("nombre", None)
        especie = data.get("especie", None)
        genero = data.get("genero", None)
        edad = data.get("edad", None)
        peso = data.get("peso", None)
    
        delivery_zoo = self.factory.create_animal(
            tipo_animal, nombre, especie, genero, edad, peso
        )
        a=IDs.id_animal()
        animales[a] = delivery_zoo
        return delivery_zoo
    
    def list_animales(self):
        return {index: animal.__dict__ for index, animal in animales.items()}
    
    def update_animal(self, animal_id, data):
        if animal_id in animales:
            animal = animales[animal_id]
            nombre = data.get("nombre", None)
            especie= data.get("especie", None)
            genero= data.get("genero", None) 
            edad= data.get("edad", None) 
            peso= data.get("peso", None)
            if nombre:
                animal.nombre = nombre
            if especie:
                animal.especie = especie
            if genero:
                animal.genero = genero
            if edad:
                animal.edad= edad
            if peso:
                animal.peso= peso
            return animal
        else:
            return None
            #raise None
    
    def delete_animal(self, animal_id):
        if animal_id in animales:
            del animales[animal_id]
            return {"message": "Vehículo eliminado"}
        else:
            return None
    
    def animal_especie(self, especie):
        return {index: animal for index, animal in animales.items() if animal["especie"]==especie}
    
    def animal_genero(self, genero):
        return {index: animal.__dict__ for index, animal in animales.items() if animal["genero"] == genero}
    
    ######## atención #########33
class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.delivery_service = ZooService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/animales":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.delivery_service.add_animal(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
    
        if self.path == "/animales":
            response_data = self.delivery_service.list_animales()
            HTTPDataHandler.handle_response(self, 200, response_data)
        elif parsed_path.path == "/animales":
            if "especie" in query_params:
                especie = query_params["especie"][0]
                animales_filtrados= ZooService.animal_especie(self, especie)
                if animales_filtrados:
                    HTTPDataHandler.handle_response(self, 200, animales_filtrados)
                else:
                    HTTPDataHandler.handle_response(self, 204, [])
            elif "genero" in query_params:            
                genero = query_params["genero"][0]
                animales_filtrados = ZooService.animal_genero(genero)
                if animales_filtrados != {}:
                    HTTPDataHandler.handle_response(self, 200, animales_filtrados)
                else:
                    HTTPDataHandler.handle_response(self, 204, [])
            else:
                HTTPDataHandler.handle_response(self, 200, animales)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.delivery_service.update_animal(animal_id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Animal no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            response_data = self.delivery_service.delete_animal(animal_id)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Animal no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, RequestHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()