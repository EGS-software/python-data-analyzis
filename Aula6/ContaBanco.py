class ContaBanco:
     
    def __init__ (self, numeroConta, tipo, dono, saldo, status, tempoContaMes):
        self.numeroConta:int = numeroConta
        self.tipo:str = tipo
        self.dono:str = dono
        self.saldo:float = saldo
        self.status:bool = status
        self.tempoContaMes:int = tempoContaMes

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

def depositar(self, valor):
    if self.status == True:
        self.saldo = self.saldo + valor
        print("Depósito realizado na conta de", self.dono)
    else:
        print("Impossível depositar em uma conta inexistente")

def sacar(self, valorsaque):
    if self.status == True:
        if self.saldo >= valorsaque:
            self.saldo = self.saldo - valorsaque
            print("Saque realizado na conta de", self.dono)
        else:
            print("Saldo insuficiente para saque")

def taxaMensal(self, tempoContaMes):
        if self.tempoContaMes >= 1:
            if self.tipo == "CC":
                self.saldo = self.saldo - 12
                print("Mensalidade de conta corrente cobrada com sucesso")
            elif self.tipo == "CP":
                self.saldo = self.saldo - 20
                print("Mensalidade de conta poupança cobrada com sucesso")
                
