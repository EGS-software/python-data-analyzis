from conexao import usar_conexao

def listar_bancos(connection):
    print("BD existentes no servidor: ")
    show_db_query = "SHOW DATABASES"
            #Cria o objeto cursor a partir da conexão
    with connection.cursor() as cursor:
                #Executa a query
                cursor.execute(show_db_query)
                #Percorre o resultado da query
                for db in cursor:
                    print(db[0])