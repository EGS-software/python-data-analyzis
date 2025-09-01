# Ler arquivo:
arquivo = open("exemplo.txt", 'r')
conteudo = arquivo.read()
print(conteudo)
arquivo.close()

# Forma na norma padrão:
with open('exemplo.txt', 'r') as arquivo:
  conteudo = arquivo.read()
  print(conteudo)

# Escrever arquivo:
with open('dados.txt', 'w') as dados:
  dados.write("Olá garotos")
  dados.write("Sou um garotão de software")

# Manipulação de arquivo CSV

import csv

#Abrir o arquivo CSV para leitura
with open('dados-csv.csv', 'r', encoding='utf-8') as entrada:
  leitor_csv = csv.reader(entrada)
  #Abrir novo arquivo para escrita
  with open('novo_dados-csv.csv', 'w', encoding='utf-8', newline='') as saida:
    escritor_csv = csv.writer(saida)
    for linha in leitor_csv:
      print(linha)
      escritor_csv.writerow(linha)

#Manipulação JSON
import json

#ABrir o arquivo JSON para leitura
with open('dados-json.json', 'r', encoding="utf-8") as entrada:
  dados = json.load(entrada)
  print(dados)
  #Abrir novo arquivo
with open('novo_dados-json.json', mode='w', encoding="utf-8") as saida
  json.dump(dados, saida, indent=4)

#EXEMPLO CRUD COM CSV
import csv

ARQ = 'produtos.csv'

def load():
  with open(ARQ, mode='r', encoding="utf-8") as f:
            return list(csv.reader(f))
def save(db):
  with open(ARQ,  mode='w', encoding="utf-8") as f:
    csv.writer(f).writerows(db)

db = load()

#C - CREATE
db.append(["3", "Produto C", "20.0"])

#R - Read
print(db)

#U - Update(alterar onde id ==1)
for linha in db:
  if linha[0] == "1": #coluna 0=id
      linha[2] == "30.0" #coluna 2=preco
save(db)


  
  


















