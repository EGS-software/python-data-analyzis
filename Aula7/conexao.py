from getpass import getpass
from mysql.connector import connect, Error

def usar_conexao(acao):
    try:
        with connect(
            host="localhost",
            user=input("Usuário: "),
            password=getpass("Senha: ")
        ) as connection:
            print("Conexão estabelecida!", connection)
            return acao(connection)

    except Error as e:
        print("Ocorreu um erro ao tentar se conectar ao banco de dados.")