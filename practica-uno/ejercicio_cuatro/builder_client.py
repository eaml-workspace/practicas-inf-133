import requests

url = "http://localhost:8000/pacientes"
headers = {"Content-type": 'application/json'}

response = requests.get(url)
print(response.json())

paciente_new = {
    "ci": 123456,
    "nombre": "Emanuel",
    "apellido": "Monzón",
    "edad": 18,
    "genero":"Masculino",
    "diagnostido":"Diabetes",
    "doctor":"Sancho-Panza"
}
response = requests.post(url, json=paciente_new, headers=headers)
print(response.json())

paciente_new = {
    "ci": 654321,
    "nombre": "Ema",
    "apellido": "Lozano",
    "edad": 50,
    "genero":"Masculino",
    "diagnostido":"Diabetes",
    "doctor":"Pedro-Pérez"
}
response = requests.post(url, json=paciente_new, headers=headers)
print(response.json())

edit_pa = {
    "diagnostico": "ENFERMEDAD!!!"
}

response = requests.put(url, json=edit_pa, headers=headers)
