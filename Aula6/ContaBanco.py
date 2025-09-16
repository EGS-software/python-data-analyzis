class ContaBanco:
     
    def __init__ (self, numeroConta, tipo, dono, saldo, status):
        self.numeroConta = numeroConta 
        self.tipo:str = tipo
        self.dono:str = dono
        self.saldo:float = saldo
        self.status:bool = status

def abrirConta(self, tipo):
    self.tipo = tipo
    self.status = True
    if tipo == "CC":
        self.saldo = 50
    elif tipo == "CP":
        self.saldo = 150 

def fecharConta(self):
    if self.saldo > 0:
        print("Conta com dinheiro, não posso fechá-la")
    elif self.saldo < 0:
        print("Conta em débito, não posso fechá-la")
    else:
        self.status = False
        print("Conta fechada com sucesso")