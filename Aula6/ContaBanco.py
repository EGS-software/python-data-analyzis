def __init__ (self, numeroConta, tipo, dono, saldo, status):
        self.numeroConta = numeroConta
        self.tipo = tipo
        self.dono = dono
        self.saldo = saldo
        self.status = status

def abrirConta(self, tipo):
    self.tipo = tipo
    self.status = True
    if tipo == "CC":
        self.saldo = 50
    elif tipo == "CP":
        self.saldo = 150    