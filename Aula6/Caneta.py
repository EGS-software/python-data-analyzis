class Caneta:
    def __init__(self, cor, modelo, carga, tampada):
        self.cor = cor
        self.modelo = modelo
        self.carga = carga
        self.tampada = tampada

    def rabiscar(self):
        if self.tampada is True:
            print("Não é possível escrever. A caneta está tampada...")
        else:
            print("A caneta está escrevendo...")

try:
    c1 = Caneta("Vermelha", "WBM-7", 100, False)
    print(c1.cor, c1.modelo, c1.carga, c1.tampada)
    c1.rabiscar()
except Exception:
    print("Erro ao criar ou usar c1")

try:
    c2 = Caneta("Azul", "QB-250", 80, True)
    print(c2.cor, c2.modelo, c2.carga, c2.tampada)
    c2.rabiscar()
except Exception:
    print("Erro ao criar ou usar c2")


    def tampar(self):
        self.tampada = True

    def destampar(self):
        self.tampada = False