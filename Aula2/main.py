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
    num_janelas = int(input("Quantas janelas existem na sala? "))
    area_total_janelas = 0
    carga_total_janelas = 0

    for i in range(num_janelas):
        print(f"\nJANELA {i+1}")
        area_janela = float(input("Informe a área da janela (em m²): "))

        print("A janela pega sol de manhã com cortina (1)")
        print("A janela pega sol de tarde com cortina (2)")
        print("A janela pega sol de manhã sem cortina (3)")
        print("A janela pega sol de tarde sem cortina (4)")
        print("A janela está na sombra (5)")
        tipo = int(input("Escolha a opção correspondente (1 a 5): "))

        # Coeficientes da Tabela 2 (linha M2 = 1)
        coeficientes = {
            1: 160,  # Sol manhã com cortina
            2: 212,  # Sol tarde com cortina
            3: 222,  # Sol manhã sem cortina
            4: 410,  # Sol tarde sem cortina
            5: 37    # Vidros na sombra
        }

        coeficiente = coeficientes.get(tipo, 0)

        carga_janela = area_janela * coeficiente
        carga_total_janelas += carga_janela
        area_total_janelas += area_janela

    num_portas = int(input("\nQuantas portas existem na sala? "))
    area_porta = float(input("Qual a área ocupada por portas (em m²)? "))
    print("Dados armazenados\n")
    return carga_total_janelas, area_porta


def coletar_dados_adicionais():
    print("-----DADOS ADICIONAIS-----")
    num_pessoas = int(input("Quantas pessoas ficarão na sala? "))
    num_equip = int(
        input("Qual a potência elétrica (em W) somada de todos os equipamentos da sala? ")
    )
    print("Dados armazenados\n")
    return num_pessoas, num_equip


def calcular_carga_termica(volume, posicao, carga_janela, area_porta, num_pessoas, num_equip):
    # Tabela 1
    if posicao == 1:
        recinto = volume * 16
    else:
        recinto = volume * 22.3

    porta = area_porta * 125
    pessoas = num_pessoas * 125
    aparelhos = num_equip * 0.9

    carga_termica = recinto + carga_janela + porta + pessoas + aparelhos
    carga_BTU = carga_termica * 3.92

    return recinto, carga_janela, porta, pessoas, aparelhos, carga_termica, carga_BTU  

def exibir_resultados(recinto, janela, porta, pessoas, aparelhos, carga_termica, carga_BTU):
    print("-----RESULTADOS DO LEVANTAMENTO-----")
    print(f"Recinto: {recinto:.2f} kcal/h")
    print(f"Janelas: {janela:.2f} kcal/h")
    print(f"Portas: {porta:.2f} kcal/h")
    print(f"Pessoas: {pessoas:.2f} kcal/h")
    print(f"Equipamentos elétricos: {aparelhos:.2f} kcal/h")
    print(f"\nCarga térmica total: {carga_termica:.2f} kcal/h")
    print(f"Carga térmica em BTUs: {carga_BTU:.2f} BTUs")
    print(
        f"\nPara refrigerar essa sala adequadamente, é necessário um AC de aproximadamente {round(carga_BTU)} BTUs"
    )


def recomendacaoAr(cargaBTU):
    print("\n---RECOMENDAÇÃO DE APARELHO---")
    if cargaBTU <= 9000:
        print("Modelo sugerido (9.000 BTUs): https://www.mercadolivre.com.br/ar-condicionado-split-hi-wall-tcl-9000-btuh-frio-monofasico-220-volts/p/MLB23378747")
    elif cargaBTU>9000 and cargaBTU<= 12000:
        print("Modelo sugerido (12.000 BTUs): https://www.magazineluiza.com.br/ar-condicionado-split-hi-wall-hitachi-air-home-600-inverter-12000-btus-quente-e-frio-r32-220v/p/eej8j6e449")
    elif cargaBTU>12000 and cargaBTU<= 18000:
        print("Modelo sugerido (18.000 BTUs): https://www.magazineluiza.com.br/ar-condicionado-split-hi-wall-inverter-lg-dual-voice-ai-18-000-btus-frio-220v-r-32/p/fe2e42gh0d")
    else:
        print("Modelo sugerido (36.000 BTUs): https://www.magazineluiza.com.br/ar-condicionado-split-pisoteto-midea-inverter-36000-btus-frio-r32-220v-midea-carrier/p/jb3k92a954")


def main():
    volume, posicao = coletar_dados_recinto()
    carga_janela, area_porta = coletar_dados_aberturas()
    num_pessoas, num_equip = coletar_dados_adicionais()

    recinto, janela, porta, pessoas, aparelhos, carga_termica, carga_BTU = calcular_carga_termica(
        volume, posicao, carga_janela, area_porta, num_pessoas, num_equip
    )

    exibir_resultados(recinto, janela, porta, pessoas, aparelhos, carga_termica, carga_BTU)
    recomendacaoAr(carga_BTU)

if __name__ == "__main__":
    main()
