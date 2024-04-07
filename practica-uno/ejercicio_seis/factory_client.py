import requests
import json

url = "http://localhost:8000/animales"
headers = {"Content-Type":"applocation/json"}

new_animal={
    "tipo_animal": "mamifero",
    "nombre": "Juanito",
    "especie": "Cocodrilo",
    "edad": 33,
    "genero":"Macho",
    "peso":50,
}
response = requests.post(url=url, json=new_animal, headers=headers)
print(response.json())
new_animal={
    "tipo_animal": "mamifero",
    "nombre": "Pipa",
    "especie": "Leon",
    "edad": 23,
    "genero":"Hembra",
    "peso":70,
}
response = requests.post(url=url, json=new_animal, headers=headers)
print(response.json())

response = requests.get(url=url)
print(response.json())

animal_id_to_update = 2
updated_animal_data = {
    "edad": "666"
}
response = requests.put(f"{url}/{animal_id_to_update}", json=updated_animal_data)
print("Animal actualizado:", response.json())

animal_id_to_delete = 1
response = requests.delete(f"{url}/{animal_id_to_delete}")
print("Animal eliminado:", response.json())

# GET /deliveries
response = requests.get(url=url)
print(response.json())