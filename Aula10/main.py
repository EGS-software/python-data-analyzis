import requests
response = requests.get("https://viacep.com.br/ws/98700000/json/")
print(response.status_code)
print(response.json())
