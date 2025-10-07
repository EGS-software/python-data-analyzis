#ID = 5 para "GOld"
from connection_mongo import user_conexao_mongo
from pymongo.errors import PyMongoError

def updateStatusCliente(db):
    filter = {"_id": 5}
    update = {"$set": {"status": "Gold"}}

    try:
        res = db.clientes.update_one(filter, update)

        print("Linhas afetadas: ", res.matched_count)
        print("Linhas modificadas: ", res.modified_count)

        doc = db.clientes.find_one(filter, {"_id": 1, "cliente":1, "status":1})
        print("Após a atualização: ", doc)
    except PyMongoError as e:
        print("Erro na atualização: ", e)

user_conexao_mongo(updateStatusCliente)