def coletar_dados_recinto():
    print("-----DADOS DO RECINTO-----")
    comprimento = float(input("Digite o comprimento da sala (em m): "))
    largura = float(input("Digite a largura da sala (em m): "))
    altura = float(input("Digite o pé direito da sala (em m): "))
    volume = comprimento * largura * altura
    posicao = int(input("A sala está entre andares (1) ou sob o telhado (2)? "))
    print("Dados armazenados\n")
    return volume, posicao


def coletar_dados_aberturas():
    print("-----DADOS DE ABERTURAS-----")
    numJanela = int(input("Quantas janelas existem na sala? "))
    areaJanela = float(input("Qual a área ocupada por essas janelas (em m2)? "))
    numPortas = int(input("Quantas portas existem na sala? "))
    areaPorta = float(input("Qual a área ocupada por portas (em m2)? "))
    print("Dados armazenados\n")
    return areaJanela, areaPorta


def coletar_dados_adicionais():
    print("-----DADOS ADICIONAIS-----")
    numPessoas = int(input("Quantas pessoas ficarão na sala? "))
    numEquip = int(
        input(
            "Qual a potência elétrica (em W) somada de todos os equipamentos da sala? "
        )
    )
    print("Dados armazenados\n")
    return numPessoas, numEquip


def calcular_carga_termica(
    volume, posicao, areaJanela, areaPorta, numPessoas, numEquip
):
    # Tabela 1
    if posicao == 1:
        recinto = volume * 16
    else:
        recinto = volume * 22.3

    janela = areaJanela * 400
    porta = areaPorta * 125
    pessoas = numPessoas * 125
    aparelhos = numEquip * 0.9

    cargaTermica = recinto + janela + porta + pessoas + aparelhos
    cargaBTU = cargaTermica * 3.92

    return recinto, janela, porta, pessoas, aparelhos, cargaTermica, cargaBTU


def exibir_resultados(
    recinto, janela, porta, pessoas, aparelhos, cargaTermica, cargaBTU
):
    print("-----RESULTADOS DO LEVANTAMENTO-----")
    print(f"Recinto: {recinto} kcal/h")
    print(f"Janelas: {janela} kcal/h")
    print(f"Portas: {porta} kcal/h")
    print(f"Pessoas: {pessoas} kcal/h")
    print(f"Equipamentos elétricos: {aparelhos} kcal/h")
    print(f"\nCarga térmica (kcal/h): {cargaTermica}")
    print(f"Carga térmica (em BTUs): {cargaBTU}")
    print(
        f"\nPara refrigerar essa sala adequadamente, é necessário um AC de {cargaBTU} BTUs"
    )


def main():
    volume, posicao = coletar_dados_recinto()
    areaJanela, areaPorta = coletar_dados_aberturas()
    numPessoas, numEquip = coletar_dados_adicionais()

    recinto, janela, porta, pessoas, aparelhos, cargaTermica, cargaBTU = (
        calcular_carga_termica(
            volume, posicao, areaJanela, areaPorta, numPessoas, numEquip
        )
    )

    exibir_resultados(
        recinto, janela, porta, pessoas, aparelhos, cargaTermica, cargaBTU
    )


if __name__ == "__main__":  # Entry point for the script
    main()
