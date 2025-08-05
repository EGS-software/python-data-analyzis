ph = float(input("Digite um valor do pH: "))

if ph < 7.0:
    print("Solução ácida")
elif ph == 7.0:
    print ("Solução neutra")
else:
    print("Solução básica")