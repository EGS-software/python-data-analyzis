# Objetivo: SELECT * FROM <tabela> LIMIT 5

from connection_mongo import user_conexao_mongo
from Aula8.consults import listar

def selectInput(db):
    colecao = db[input("Coleção: ")]
    for doc in colecao.find().limit(5):
        print(doc)


user_conexao_mongo(selectInput)
