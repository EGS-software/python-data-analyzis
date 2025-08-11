print('-----DADOS DO RECINTO-----')
comprimento = float(input("Digite o comprimento da sala (em m): "))
largura = float(input("Digite a largura da sala (em m): "))
altura = float(input('Digite o pé direito da sala (em m): '))
volume = comprimento * largura * altura
posicao = int(input('A sala está entre andares (1) ou sob o telhado (2)? '))
print('Dados armazenados\n')

print('-----DADOS DE ABERTURAS-----')
numJanela = int(input('Quantas janelas existem na sala? '))
areaJanela = float(input('Qual a área ocupada por essas janelas (em m2)? '))
numPortas = int(input('Quantas portas existem na sala? '))
areaPorta = int(input('Qual a área ocupada por portas (em m2)? '))
print('Dados armazenados\n')

print('-----DADOS ADICIONAIS-----')
numPessoas = int(input('Quantas pessoas ficarao na sala? '))
numEquip = int(input('Qual a potencia elétrica (em W) somada de todos os equipamentos da sala? '))
print('Dados armazenados\n')

# Tabela 1
# kcal/h referente ao volume da sala (m3)
# entre andares = 16 kcal/m3        sob telhado = 22.3 kcal/m3

if(posicao == 1):
    recinto = volume * 16
else:
    recinto = volume * 22.3

# kcal/h referente a area de janelas
janela = areaJanela * 400

# kcal/h referente a portas
porta = areaPorta * 125

# kcal/h referente a pessoas
pessoas = numPessoas * 125

# kcal/h referente a aparelhos
aparelhos = numEquip * 0.9

cargaTermica = recinto + janela + porta + pessoas + aparelhos
cargaBTU = cargaTermica * 3.92

print('-----RESULTADOS DO LEVANTAMENTO-----')
print('Recinto: ' + str(recinto) + 'kcal/h')
print('Janelas: ' + str(janela) + 'kcal/h')
print('Portas: ' + str(porta) + 'kcal/h')
print('Pessoas: ' + str(pessoas) + 'kcal/h')
print('Equipamentos eletricos: ' + str(aparelhos) + 'kcal/h')
print('\nCarga termica (kcal/h): ' + str(cargaTermica))
print('Carga termica (em BTUs): ' + str(cargaBTU))
print('\nPara refrigerar essa sala adequadamente, e necessario um AC de ' + str(cargaBTU) + 'BTUs')