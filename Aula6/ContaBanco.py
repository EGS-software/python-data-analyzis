class ContaBanco:
     
    def __init__ (self, numeroConta, tipo, dono, saldo, status):
        self.numeroConta:int = numeroConta
        self.tipo:str = tipo
        self.dono:str = dono
        self.saldo:float = saldo
        self.status:bool = status

def abrirConta(self, tipo):
    self.tipo = tipo
    self.status = True
    if tipo == "CC":
       if self.saldo >= 36:
        self.saldo = self.saldo - 12 
        print("Conta Corrente aberta com sucesso")
    elif tipo == "CP":
        if self.saldo >= 60:
            self.saldo = self.saldo - 20
        print("Conta Poupança aberta com sucesso") 

def fecharConta(self):
    if self.saldo > 0:
        print("Conta com dinheiro, não posso fechá-la")
    elif self.saldo < 0:
        print("Conta em débito, não posso fechá-la")
    else:
        self.status = False
        print("Conta fechada com sucesso")