# Objetivo: SELECT * FROM <tabela> LIMIT 5

from connection_mongo import use_connection_mongo

def selectInput(db):
    colecao = db[input("Coleção: ")]
    for doc in colecao.find().limit(5):
        print(doc)


use_connection_mongo(selectInput)
