import requests

url = "http://localhost:8000/"

ruta_get= url + "animales"

get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
# POST agrega un nuevo paciente por la ruta /pacientes
ruta_post = url + "animales"
nuevo_paciente = {
    "id": 1,
    "nombre": "Juanito",
    "especie": "Panda",
    "edad": 33,
    "genero":"Macho",
    "peso":50,
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_paciente)
print(post_response.text)

ruta_put= url + "animales/1"
animal_put={
    "peso":70,
    "edad":35
}
update_response= requests.request(method="PUT", url=ruta_put, json=animal_put)
print(update_response.text)

ruta_del = url + "animales/2"
response = requests.request(method="DELETE", url = ruta_del)
print(response.text)

# GET filtrando por nombre con query params
ruta_get = url + "animales?especie=Panda"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
ruta_get = url + "animales?genero=Masculino"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)