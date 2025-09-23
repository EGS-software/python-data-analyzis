from conexao import usar_conexao

def listar_bancos(connection):
            #Cria o objeto cursor a partir da conexão
    with connection.cursor() as cursor:
                #Executa a query
                cursor.execute("SHOW DATABASES")
                #Percorre o resultado da query
                for db in cursor:
                    print(db[0])

usar_conexao(listar_bancos)