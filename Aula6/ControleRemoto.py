class ControleRemoto:
    def __init__(self, color, height, largura, profundidade):
        self.color:str = color
        self.height = height
        self.largura = largura
        self.profundidade = profundidade

def alterar_temperatura(self, botao):
    if botao == "+":
        print ("Aumentando a temperatura")
    elif botao == "-":
        print ("Diminuindo a temperatura")

controle_remoto1 = ControleRemoto("branco", "8cm", "4cm", "1cm")
print(controle_remoto1.color, controle_remoto1.height, controle_remoto1.largura, controle_remoto1.profundidade)

controle_remoto2 = ControleRemoto("cinza", "10cm", "3cm", "2cm")
print(controle_remoto1.color, controle_remoto1.height, controle_remoto1.largura, controle_remoto1.profundidade)

controle_remoto1.alterar_temperatura("+")
controle_remoto1.alterar_temperatura("-")

# Caracteristicas
#------
#------
#------

# Metodos

#-----
#-----
#-----