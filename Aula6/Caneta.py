class caneta:
    def __init__(self, cor, ponta, carga, tampada):
        self.cor = cor
        self.ponta = ponta
        self.carga = carga
        self.tampada = tampada

    def rabiscar(self):
        if self.tampada:
            print("ERRO! Nao posso rabiscar")
        else:
            print("Estou rabiscando")

    def tampar(self):
        self.tampada = True

    def destampar(self):
        self.tampada = False