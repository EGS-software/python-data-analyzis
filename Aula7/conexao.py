from getpass import getpass
from mysql.connector import connect

try:
    with connect(
        host="localhost",
        user=input("Usuário: "),
        password=getpass("Senha: ")
    ) as connection:
        print("Conexão estabelecida!")

except:
    print("Ocorreu um erro ao tentar se conectar ao banco de dados.")