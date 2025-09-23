from conexao import usar_conexao

def inserir_vendedores(connection):
    #Usamos 3 """ para permitir quebras de linha na query"
    insert_query = """ 
    INSERT INTO Vendedores(Nome) VALUES
        ('João Alfredo Williges Cunha')
    """
    with connection.cursor() as cursor:
        #Aqui deve-se colocar o nome do banco correto após o USE
        cursor.execute("USE bdSegunda")
        cursor.execute(insert_query)
        connection.commit()
        print("Vendedor inserido com sucesso!")

usar_conexao(inserir_vendedores)