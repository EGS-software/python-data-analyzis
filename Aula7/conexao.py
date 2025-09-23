from getpass import getpass
from mysql.connector import connect

try:
    with connect(
        host="localhost",
        user=input("Usuário: "),
        password=getpass("Senha: ")
    ) as connection:
        print("Conexão estabelecida!")

        print("BD existentes no servidor: ")
        show_db_query = "SHOW DATABASES"
        #Cria o objeto cursor a partir da conexão
        with connection.cursor() as cursor:
            #Executa a query
            cursor.execute(show_db_query)
            #Percorre o resultado da query
            for db in cursor:
                print(db[0])

except:
    print("Ocorreu um erro ao tentar se conectar ao banco de dados.")