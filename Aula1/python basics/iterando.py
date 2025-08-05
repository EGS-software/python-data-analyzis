nomes = ["Ana", "Bruno", "Carlos"];

for nome in nomes:
    print("Olá, ", nome);

#Soma
soma = 0;
for i in range(1, 6):
    soma += i;
print("Soma:", soma);

#Break
for i in range(10):
    if i == 5:
        break
print(i);

#Continue
for i in range(5):
    if i == 2:
        continue;
print(i);