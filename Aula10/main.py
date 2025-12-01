import requests

# using get to consume the api from viacep.com.br#
response = requests.get("https://viacep.com.br/ws/98700000/json/")
print(response.status_code)
print(response.json())


#func to consult dollar price
def consultar_dolar():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    response = requests.get(url)
    dados = response.json()
    # A AwesomeAPI retorna um dicionário com a chave "USDBRL"
    cotacao = dados.get( "USDBRL")
    print( f"Conversão : {cotacao.get( 'name', '')}")
    print( f"Compra : {cotacao.get( 'bid', '')}")
    print( f"Venda : {cotacao.get( 'ask', '')}")
    print( f"Atualizado em: {cotacao.get( 'create_date' , '')}")
consultar_dolar()