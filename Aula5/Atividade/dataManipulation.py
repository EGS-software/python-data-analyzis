import csv
from collections import defaultdict
from datetime import datetime


entrada = 'sales_data.csv'

dados = []
with open (entrada, 'r', encoding='utf-8') as f:
    leitor = csv.DictReader(f, delimiter=',')
    for linha in leitor:
        produto = linha["Produto"]
        categoria = linha["Categoria"]
        preco = float(linha["Preço Unitário (R$)"])
        qtd = int(linha["Quantidade Vendida"])
        total = float(linha["Total de Vendas (R$)"])
        data = linha["Data da Venda"]
        dados.append({
            "produto": produto,
            "categoria": categoria,
            "preco": preco,
            "qtd": qtd,
            "total": total,
            "data": data
        })

# Resumo por Categoria
resumo_categoria = defaultdict(float)
for item in dados:
    resumo_categoria[item["categoria"]] += item["total"]

with open('resumo_categoria.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Categoria', 'Total Vendido (R$)'])
    for categoria, total in resumo_categoria.items():
        writer.writerow([categoria, f'{total:.2f}'])

print("Categoria,TotalVendido")
for categoria, total in resumo_categoria.items():
    print(f"{categoria},{total:.2f}")


# Cinco produtos mais vendidos por categoria
vendas_produto_cat = defaultdict(lambda: defaultdict(float))
for item in dados:
    vendas_produto_cat[item["categoria"]][item["produto"]] += item["total"]

with open('mais_vendidos.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Categoria', 'Produto', 'Total Vendido (R$)'])
    for categoria, produtos in vendas_produto_cat.items():
        top5 = sorted(produtos.items(), key=lambda x: x[1], reverse=True)[:5]
        for produto, total in top5:
            writer.writerow([categoria, produto, f'{total:.2f}'])

print("\nCategoria,Produto,TotalVendas")
for categoria, produtos in vendas_produto_cat.items():
    top5 = sorted(produtos.items(), key=lambda x: x[1], reverse=True)[:5]
    for produto, total in top5:
        print(f"{categoria},{produto},{total:.2f}")


# Mês com maior faturamento

faturamento_mensal = defaultdict(float)
for item in dados:
    dt = datetime.strptime(item["data"], '%Y-%m-%d')
    mes_ano = dt.strftime('%m/%Y')
    faturamento_mensal[mes_ano] += item["total"]

mes_campeao = max(faturamento_mensal.items(), key=lambda x: x[1])

with open('mes_campeao.csv', 'w', newline='', encoding='utf-8') as f:
    f.write(f'Mês campeão: {mes_campeao[0]} - Faturamento: R$ {mes_campeao[1]:.2f}\n')

print("\nmes_campeao.txt")
print(f"{mes_campeao[0]},{mes_campeao[1]:.2f}")