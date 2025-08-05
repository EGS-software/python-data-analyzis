soma = 0 

x = int(input("Digite um valor (0 para sair): "))

while x != 0:
    soma += x
    x= int(input("Digite um valor (0 para sair: )"))

print("Soma total: ", soma)

while True:
    x = int(input("Digite um valor (0 para sair): "))

    if x <= 0:
        continue
    print("Valor Positivo:", x)
    break

while True:
    x = int(input("Digite um valor (0 para sair): "))

    if x == 0:
        break
    print("valor lido", x)
