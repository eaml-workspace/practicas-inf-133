import requests

url = "http://localhost:8000/"

ruta_get= url + "pacientes"

get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
# POST agrega un nuevo paciente por la ruta /pacientes
ruta_post = url + "pacientes"
nuevo_paciente = {
    "ci": 14488141,
    "nombre": "Juanito",
    "apellido": "Pérez",
    "edad": 33,
    "genero":"Masculino",
    "diagnostico":"Diabetes",
    "doctor":"Pedro-Pérez",
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_paciente)
print(post_response.text)

# GET filtrando por nombre con query params
ruta_get = url + "pacientes/?doctor=Pedro-Pérez"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
ruta_get = url + "pacientes?diagnostico=Diabetes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)