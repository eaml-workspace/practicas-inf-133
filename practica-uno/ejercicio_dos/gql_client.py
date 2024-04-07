import requests
# Definir la URL del servidor GraphQL
url = 'http://localhost:8000/graphql'

query_lista="""
    {
        plantas {
            id
            nombre
            especie
            edad
            altura
            fruto
        }
    }
"""
response = requests.post(url, json={'query': query_lista})
print(response.text)

query_especie="""
    {
        plantasPorEspecie(especie: "Cactaceae") {
            plantas {
                id
                nombre
                edad
                altura
                fruto
            }
        }
    }
"""
response_especie = requests.post(url, json={'query': query_especie})
print(response_especie.text)

query_fruto="""
    {
        plantasPorFruto(fruto: True) {
            plantas {
                id
                nombre
                especie
                edad
                altura
            }
        }
    }
"""
response_fruto= requests.post(url, json={'query': query_fruto})
print(response_fruto.text)

# Definir la consulta GraphQL para crear nuevo estudiante
query_crear = """
mutation {
        crearPlanta(nombre: "Rosa", especie: "Rosaceae", edad: 1, altura: 30, fruto: False) {
            plantas {
                id
                nombre
                especie
                edad
                altura
                fruto
            }
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_crear})
print(response_mutation.text)

# Definir la consulta GraphQL para eliminar un estudiante
query_eliminar = """
mutation {
        deletePlanta(id: 2) {
            plantas {
                id
                nombre
                especie
                edad
                altura
                fruta
            }
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_eliminar})
print(response_mutation.text)

query_actualizar="""
mutation{
        actualizarPlanta(id: 1, altura: 205){
            plantas{
                id
                nombre
                especie
                altura
            }
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_actualizar})
print(response_mutation.text)