
while True:
    print ("Ligando...")
    ligacao = input("Ligação atendida? (sim/não)")
    if ligacao == "não":
        print ("Ligação não atendida, tentando novamente")
    else:
        break


print ("Convidando para refeição...")
convite = input ("Convite aceito? (sim/não)")

if convite == "sim":
    print("Amizade começou")
    exit()
else:
    print ("Convidando para bebida")
    bebida = input("Convite aceito? (sim/não)")

if bebida == "sim":
    opcoes = ["1 - Café", "2 - Chá", "3 - Chocolate" ]
    for opcao in opcoes:
         print(opcao)
    escolha = input ("Escolha uma bebida : ").strip()
    print (f"Bebida escolhida {opcoes[int(escolha)-1]}")
    print ("Amizade começou")
    exit()
else: 
     
    interesse = print("Verificando interesse")
    opcoes = ["1 - Café", "2 - Chá", "3 - Chocolate" ]
    for opcao in opcoes:
        interesse = input(f"Tem interesse (sim/não) {opcao} ").strip().lower()
        if interesse == "sim":
            gostou = input("Gostou? (sim/não) ")
            if gostou == "sim":
                print ("Amizade começou")
                exit()
            else:
                continue

        



