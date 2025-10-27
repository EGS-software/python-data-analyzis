import numpy as np

# Vetor de nomes das cidades
cidades = np.array(["Augusto Pestana", "Santa Rosa", "Ijuí"])

dias = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]

# Matriz 3x7 com temperaturas fictícias
primeira_semana = np.array([
    [20,21,23,26,28,27,25],
    [16,18,21,25,27,26,22],
    [17,19,22,24,26,25,21]
])

#Ajuste pontual
primeira_semana[2,2] = 18
print(primeira_semana)

#Construção da 2° Semana
ajuste_chuva = np.array([0,-5,-5,-5,-2,-2,-2])
segunda_semana = primeira_semana + ajuste_chuva
print(segunda_semana)

#Construção terceira semana(massa de ar seco)
