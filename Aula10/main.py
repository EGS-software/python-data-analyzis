import requests

# using get to consume the api from viacep.com.br#
response = requests.get("https://viacep.com.br/ws/98700000/json/")
print(response.status_code)
print(response.json())
