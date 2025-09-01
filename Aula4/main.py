# Ler arquivo:
arquivo = open("exemplo.txt", 'r');
conteudo = arquivo.read();
print(conteudo);
arquivo.close();

# Forma na norma padrão:
with open('exemplo.txt', 'r') as arquivo:
  conteudo = arquivo.read();
  print(conteudo);

# Escrever arquivo:
with open(dados.txt, 'w') as dados:
  arquivo.write("Olá garotos");
  arquivo.write("Sou um garotão de software");

# Manipulação de arquivo CSV

import csv

#Abrir o arquivo CSV para leitura
with open('dados-csv.csv', 'r', 'utf-8') as entrada:
  leitor_csv = csv.reader(entrada);





