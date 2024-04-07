import requests

url = "http://localhost:8000/"

# GET /player
response = requests.request(method="GET", url=url + "partidas")
print(response.text)

# POST /player/damage
response = requests.request(
    method="POST", url=url + "partidas/elemento", json={"elemento": "tijera"}
)
print(response.text)