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
ajuste_ar = 10
terceira_semana = segunda_semana + ajuste_ar
print(terceira_semana)

#Agrupar as 3 semanas
semanas = [primeira_semana + segunda_semana + terceira_semana]

for i, temperatura_semana in enumerate(semanas, 1):
    medias = temperatura_semana.mean(axis=1)

    # np.argsort(medias) retorna os indices que ordenam em ordem crescente
    # [:: -1] inverte a ordenação
    ordem = np.argsort(medias)[:: -1]

    print(f"\nSemana {i} = Ranking de temperatura média: ")

    for pos, idx in enumerate(ordem, 1):
        print(f"\n{pos}° {cidades[idx]} ({medias[idx]:.2f}°C)")
