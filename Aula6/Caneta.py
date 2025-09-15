class caneta:
    def __init__(self, cor, ponta, carga, tampada):
        self.cor = cor
        self.ponta = ponta
        self.carga = carga
        self.tampada = tampada

    def rabiscar(self):
        if self.tampada is True:
            print("Não é possível escrever. A caneta está tampada...")
        else:
            print("A caneta está escrevendo...")

    def tampar(self):
        self.tampada = True

    def destampar(self):
        self.tampada = False