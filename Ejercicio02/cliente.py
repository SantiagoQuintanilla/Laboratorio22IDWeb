import requests

params = {"limit": 10, "offset": 0}

r = requests.get("https://pokeapi.co/api/v2/pokemon", params=params)

data = r.json()

for pokemon in data["results"]:
    print(pokemon["name"])