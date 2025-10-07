#Objetivo: Listar BDs disponiveis no servidor MongoDB
#Dentro DBVEN listar coleções

from connection_mongo import user_conexao_mongo

def listar(db):
    # Listar todos os BDs do servidor
    print ("Databases: ", db.client.list_database_names())

    # Listar todas as coleções do DB
    print ("Coleções em dbven: ", db.list_collection_names())

user_conexao_mongo(listar)