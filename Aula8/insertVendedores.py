# Objetivo: inserir um documento a coleção vendedores

from connection_mongo import user_conexao_mongo

from pymongo.errors import DuplicateKeyError

def insertSeller(db):
    new_id = 11
    name = input("Digite o nome do vendedor: ")

    try:
        db.vendedores.insert_one({"_id": new_id, 
                                    "nome": name})
        print("Vendedor inserido com sucesso!")
    except DuplicateKeyError as e:
        print(f"Já existe um vendedor com esse id={new_id}. Encontre outro ID", e)

user_conexao_mongo(insertSeller)