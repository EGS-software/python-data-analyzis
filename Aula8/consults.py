#Objetivo: Listar BDs disponiveis no servidor MongoDB
#Dentro DBVEN listar coleções

from connection_mongo import use_connection_mongo

def listar(db):
    # Listar todos os BDs do servidor
    print ("Databases: ", db.client.list_database_names())

    # Listar todas as coleções do DB
    print ("Coleções em dbven: ", db.list_collection_names())

use_connection_mongo(listar)