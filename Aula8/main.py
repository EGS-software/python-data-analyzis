from pymongo import MongoClient

def user_conexao_mongo(acao, uri="mongodb://localhost:27017", dbname="dbven"):
    try:
        with MongoClient(uri) as client:
            db = client [dbname]
            print (f"Conectado a {uri} / db={dbname}") 
            return acao(db)

    except Exception as e:
        print("Erro ao conectar/usar o MongoDB", e)
