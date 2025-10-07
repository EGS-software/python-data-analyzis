# Objetivo: SELECT * FROM <tabela> LIMIT 5

from connection_mongo import user_conexao_mongo
from Aula8.consults import listar

def selectInput(db):
    colecao = db[input("Coleção: ")]
    for doc in colecao.find().limit(5):
        print(doc)

def selectAll(db):
    colecctions = ["vendedores", "produtos", "clientes", "vendas", "itensVenda"]
    for col in colecctions:
        print(f"\n--- {col} (5 documentos)---")
        # find({}) => retorna todos os docs
        #limit(5) => restring 5 docs
        cursor=db[col].find({}).limit(5)

        docs = list(cursor)

        #Se a coleçaão estiver vazia, informa
        if not docs:
            print("Sem documentos")
        else: 
            for d in docs:
                print(d)

user_conexao_mongo(selectInput)
user_conexao_mongo(selectAll)