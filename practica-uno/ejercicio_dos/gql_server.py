from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, List, Boolean, Schema, Field, Mutation

class Planta(ObjectType):
    id=Int()
    nombre=String()
    especie=String()
    edad=Int()
    altura=Int()
    fruto=Boolean()

class Query(ObjectType):
    plantas = List(Planta)
    plantas_por_especie = Field(List(Planta), especie=String())
    plantas_por_fruto = Field(List(Planta), fruto=Boolean())
    
    def resolve_plantas(root, info):
        return plantas
    
    def resolve_plantas_por_fruto(root, info, fruto):
        for planta in plantas:
            if planta.fruto==fruto:
                lista_por_frutos.append(planta)
        return lista_por_frutos
    
    def resolve_plantas_por_especie(root, info, especie):
        for planta in plantas:
            if planta.especie==especie:
                lista_por_especies.append(planta)
        return lista_por_especies

class CrearPlanta(Mutation):
    class Arguments:
        nombre=String()
        especie=String()
        edad=Int()
        altura=Int()
        fruto=Boolean()

    planta = Field(Planta)

    def mutate(root, info, nombre, especie, edad, altura, fruto):
        nueva_planta = Planta(
            id=len(plantas) + 1, 
            nombre=nombre, 
            especie=especie,
            edad=edad,
            altura=altura,
            fruto=fruto
        )
        plantas.append(nueva_planta)

        return CrearPlanta(planta=nueva_planta)

class DeletePlanta(Mutation):
    class Arguments:
        id = Int()

    planta = Field(Planta)

    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta=planta)
        return None

class ActualizarPlanta(Mutation):
    class Argument:
        id=Int()
        edad=Int()
        altura=Int()

    planta = Field(Planta)

    def mutate(root, info, id,edad, altura):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                planta.edad = edad
                planta.altura = altura
                return ActualizarPlanta(planta=planta)
        return None


class Mutations(ObjectType):
    crear_planta = CrearPlanta.Field()
    delete_planta = DeletePlanta.Field()
    actualizar_planta = ActualizarPlanta.Field()

plantas=[
    Planta(
        id=1, nombre="Cactus", especie="Cactaceae", edad=20, altura=100, fruto=True
    ),
    Planta(
        id=2, nombre="Potus", especie="Epipremnum aureum", edad=20, altura=60, fruto=False
    ),
]
lista_por_frutos=[]
lista_por_especies=[]

schema = Schema(query=Query, mutation=Mutations)


class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            print(data)
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()
