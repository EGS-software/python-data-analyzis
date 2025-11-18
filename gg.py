import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import os
import sys

print("--- INICIANDO SCRIPT DE RELATÓRIO FINAL SIASUS (v5 - Correção Final 'fantasia') ---")

# --- 1. DEFINIÇÃO DE TODAS AS QUERIES (COM NOMES) ---

print("Definindo 17 queries SQL (com todos os nomes de tradução corretos)...")

# Etapa 3.1
sql_por_trimestre = """
SELECT T.anotri AS "Ano_Trimestre", COUNT(*) AS "Total_de_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual",
    SUM(P.pa_valapr) AS "Valor_Total_Aprovado"
FROM pars AS P JOIN DIMTEMPO AS T ON P.pa_cmp = T.anomes
GROUP BY T.anotri ORDER BY T.anotri DESC;
"""
sql_por_mes = """
SELECT T.MAExt AS "Mes_Ano", COUNT(*) AS "Total_de_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual",
    SUM(P.pa_valapr) AS "Valor_Total_Aprovado"
FROM pars AS P JOIN DIMTEMPO AS T ON P.pa_cmp = T.anomes
GROUP BY T.MAExt, T.mes ORDER BY T.mes DESC;
"""

# ---
# ⚠️ Etapa 3.2 - CORRIGIDO para 'E.fantasia'
# ---
sql_por_estabelecimento = """
SELECT
    P.pa_coduni AS "Codigo_Estabelecimento",
    E.fantasia AS "Nome_Estabelecimento", 
    SUM(P.pa_qtdpro) AS "Total_Qtd_Produzida", SUM(P.pa_qtdapr) AS "Total_Qtd_Aprovada",
    ROUND((SUM(P.pa_valapr) * 100.0 / SUM(SUM(P.pa_valapr)) OVER ()), 2) AS "Pct_Valor_Total",
    SUM(P.pa_valpro) AS "Valor_Total_Produzido", SUM(P.pa_valapr) AS "Valor_Total_Aprovado"
FROM pars AS P
LEFT JOIN CADGERRS AS E ON P.pa_coduni = E.cnes
GROUP BY P.pa_coduni, E.fantasia
ORDER BY Valor_Total_Aprovado DESC;
"""

# Etapa 3.3
sql_perfil_demografico = """
SELECT
    pa_sexo AS "Sexo",
    CASE
        WHEN pa_idade <= 9 THEN '0-9 anos' WHEN pa_idade BETWEEN 10 AND 19 THEN '10-19 anos'
        WHEN pa_idade BETWEEN 20 AND 29 THEN '20-29 anos' WHEN pa_idade BETWEEN 30 AND 39 THEN '30-39 anos'
        WHEN pa_idade BETWEEN 40 AND 49 THEN '40-49 anos' WHEN pa_idade BETWEEN 50 AND 59 THEN '50-59 anos'
        WHEN pa_idade >= 60 THEN '60+ anos' ELSE 'Idade Desconhecida'
    END AS "Faixa_Etaria",
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual"
FROM pars
GROUP BY Sexo, Faixa_Etaria ORDER BY Total_Procedimentos DESC;
"""
sql_top_diagnosticos = """
SELECT
    P.pa_cidpri AS "Codigo_CID", S.cd_descr AS "Nome_Diagnostico", 
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual"
FROM pars AS P
LEFT JOIN s_cid AS S ON P.pa_cidpri = S.cd_cod
GROUP BY P.pa_cidpri, S.cd_descr
ORDER BY Total_Procedimentos DESC LIMIT 20;
"""
sql_proc_cronicos_hipertensao = """
SELECT
    P.pa_proc_id AS "Codigo_Procedimento",
    T.NO_PROCED AS "Nome_Procedimento",
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual_do_Filtro"
FROM pars AS P
LEFT JOIN TB_SIGTAW AS T ON P.pa_proc_id = T.CO_PROCED
WHERE P.pa_cidpri BETWEEN 'I10' AND 'I15'
GROUP BY P.pa_proc_id, T.NO_PROCED
ORDER BY Total_Procedimentos DESC LIMIT 20;
"""

# Etapa 3.4
sql_fluxo_top_municipios = """
SELECT
    P.pa_munpcn AS "Codigo_Municipio", M.ds_nome AS "Nome_Municipio", 
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual"
FROM pars AS P
LEFT JOIN tb_municip AS M ON P.pa_munpcn = M.co_municip
GROUP BY P.pa_munpcn, M.ds_nome
ORDER BY Total_Procedimentos DESC LIMIT 30;
"""
sql_fluxo_ijui_vs_outros = """
SELECT
    CASE
        WHEN pa_munpcn = '431490' THEN 'Morador de Ijuí'
        WHEN pa_munpcn = '999999' THEN 'Não Informado'
        WHEN pa_munpcn IS NULL THEN 'Não Informado'
        ELSE 'Morador de Outros Municípios'
    END AS "Origem_Paciente",
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual",
    SUM(pa_valapr) AS "Valor_Total_Aprovado"
FROM pars
GROUP BY Origem_Paciente ORDER BY Total_Procedimentos DESC;
"""
# ---
# ⚠️ Etapa 3.4 - CORRIGIDO para 'E.fantasia'
# ---
sql_fluxo_estab_dependentes = """
SELECT
    P.pa_coduni AS "Codigo_Estabelecimento",
    E.fantasia AS "Nome_Estabelecimento",
    P.pa_munpcn AS "Codigo_Municipio_Paciente",
    M.ds_nome AS "Nome_Municipio_Paciente",
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual_do_Filtro"
FROM pars AS P
LEFT JOIN tb_municip AS M ON P.pa_munpcn = M.co_municip
LEFT JOIN CADGERRS AS E ON P.pa_coduni = E.cnes
WHERE P.pa_munpcn != '431490' AND P.pa_munpcn != '999999'
GROUP BY P.pa_coduni, E.fantasia, P.pa_munpcn, M.ds_nome
ORDER BY Total_Procedimentos DESC LIMIT 50;
"""

# Etapa 3.5
sql_financeiro_total_ijui = """
SELECT
    'Moradores de Ijuí' AS Foco_Analise,
    SUM(pa_valapr) AS "Valor_Total_Aprovado_SUS",
    SUM(pa_valpro) AS "Valor_Total_Produzido",
    SUM(pa_valpro) - SUM(pa_valapr) AS "Diferenca_Financeira"
FROM pars
WHERE pa_munpcn = '431490';
"""
sql_financeiro_evolucao_media = """
SELECT
    T.MAExt AS "Mes_Ano",
    AVG(P.pa_valapr) AS "Gasto_Medio_Aprovado",
    AVG(P.pa_valpro) AS "Gasto_Medio_Produzido"
FROM pars AS P
JOIN DIMTEMPO AS T ON P.pa_cmp = T.anomes
GROUP BY T.MAExt, T.mes ORDER BY T.mes;
"""

# Etapa 3.6
sql_foco_oncologia = """
SELECT
    P.pa_cidpri AS "Codigo_CID",
    S.cd_descr AS "Nome_Diagnostico",
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual_do_Filtro",
    SUM(P.pa_valapr) AS "Valor_Total_Aprovado",
    SUM(P.pa_valpro) AS "Valor_Total_Produzido"
FROM pars AS P
LEFT JOIN s_cid AS S ON P.pa_cidpri = S.cd_cod
WHERE P.pa_cidpri BETWEEN 'C00' AND 'D48'
GROUP BY P.pa_cidpri, S.cd_descr
ORDER BY Valor_Total_Aprovado DESC LIMIT 20;
"""
sql_foco_saude_mental = """
SELECT
    P.pa_cidpri AS "Codigo_CID",
    S.cd_descr AS "Nome_Diagnostico",
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual_do_Filtro",
    SUM(P.pa_valapr) AS "Valor_Total_Aprovado",
    SUM(P.pa_valpro) AS "Valor_Total_Produzido"
FROM pars AS P
LEFT JOIN s_cid AS S ON P.pa_cidpri = S.cd_cod
WHERE P.pa_cidpri BETWEEN 'F00' AND 'F99'
GROUP BY P.pa_cidpri, S.cd_descr
ORDER BY Valor_Total_Aprovado DESC LIMIT 20;
"""
sql_foco_diabetes = """
SELECT
    P.pa_proc_id AS "Codigo_Procedimento",
    T.NO_PROCED AS "Nome_Procedimento",
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual_do_Filtro",
    SUM(P.pa_valapr) AS "Valor_Total_Aprovado"
FROM pars AS P
LEFT JOIN TB_SIGTAW AS T ON P.pa_proc_id = T.CO_PROCED
WHERE P.pa_cidpri BETWEEN 'E10' AND 'E14'
GROUP BY P.pa_proc_id, T.NO_PROCED
ORDER BY Total_Procedimentos DESC LIMIT 20;
"""

# Etapa 3.7
sql_comp_regional = """
SELECT
    CASE
        WHEN pa_munpcn = '431490' THEN 'Ijuí'
        WHEN pa_munpcn = '431720' THEN 'Santa Rosa'
        WHEN pa_munpcn = '430610' THEN 'Cruz Alta'
    END AS "Municipio",
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual_do_Filtro",
    SUM(pa_valapr) AS "Valor_Total_Aprovado"
FROM pars
WHERE pa_munpcn IN ('431490', '431720', '430610')
GROUP BY Municipio ORDER BY Valor_Total_Aprovado DESC;
"""
sql_tendencia_demanda_regional = """
SELECT
    T.MAExt AS "Mes_Ano",
    CASE
        WHEN P.pa_munpcn = '431490' THEN 'Ijuí'
        ELSE 'Outros Municípios (Regional)'
    END AS "Grupo_Regional",
    COUNT(*) AS "Total_Procedimentos"
FROM pars AS P
JOIN DIMTEMPO AS T ON P.pa_cmp = T.anomes
WHERE P.pa_munpcn != '999999'
GROUP BY T.MAExt, T.mes, Grupo_Regional ORDER BY T.mes, Grupo_Regional;
"""
sql_tendencia_idosos_criticos = """
SELECT
    T.MAExt AS "Mes_Ano",
    CASE
        WHEN P.pa_cidpri BETWEEN 'I00' AND 'I99' THEN 'Cardiologia'
        WHEN P.pa_cidpri BETWEEN 'C00' AND 'D48' THEN 'Oncologia'
    END AS "Area_Critica",
    COUNT(*) AS "Total_Procedimentos"
FROM pars AS P
JOIN DIMTEMPO AS T ON P.pa_cmp = T.anomes
WHERE P.pa_idade >= 60
    AND ((P.pa_cidpri BETWEEN 'I00' AND 'I99') OR (P.pa_cidpri BETWEEN 'C00' AND 'D48'))
GROUP BY T.MAExt, T.mes, Area_Critica ORDER BY T.mes, Area_Critica;
"""

# --- 2. CONFIGURAÇÃO DA CONEXÃO ---
try:
    # 
    # ⚠️ ATENÇÃO: COLOQUE SUA SENHA DO MYSQL AQUI ⚠️
    # 
    engine = create_engine("mysql+mysqlconnector://root:Tiag123!@localhost:3306/siasus")
    
    with engine.connect() as conexao:
        print("\n✅ Conexão com o banco 'siasus' realizada com sucesso!")

except Exception as e:
    print(f"\n❌ Erro fatal ao conectar ao MySQL: {e}")
    print("--- \nPOR FAVOR, VERIFIQUE SUA SENHA NA LINHA create_engine() ---")
    sys.exit() # Para o script se a conexão falhar

# --- 3. CRIAÇÃO DE UMA PASTA PARA OS RESULTADOS ---
output_dir = "resultados_analise_siasus"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
print(f"\nResultados serão salvos na pasta: '{output_dir}'")

# --- 4. FUNÇÃO AUXILIAR PARA EXECUTAR E SALVAR ---
def executar_e_salvar(nome_analise, sql_query, nome_arquivo_csv):
    """Executa uma query, printa o head e salva o resultado em CSV."""
    print(f"\n--- Iniciando Análise: {nome_analise} ---")
    try:
        df = pd.read_sql(sql_query, engine)
        print(df.head()) # Mostra as 5 primeiras linhas
        
        caminho_arquivo = os.path.join(output_dir, nome_arquivo_csv)
        # Salva em CSV com separador ';' e codificação correta para Excel
        df.to_csv(caminho_arquivo, index=False, sep=';', encoding='utf-8-sig')
        print(f"    -> Sucesso! Resultado salvo em: {nome_arquivo_csv}")
        return df # Retorna o dataframe para plotagem, se necessário
        
    except Exception as e:
        print(f"    -> ❌ ERRO ao executar a análise '{nome_analise}': {e}")
        return None

# --- 5. EXECUÇÃO DE TODAS AS ANÁLISES ---

# Mapeia todas as análises para suas queries e nomes de arquivo
mapa_analises = {
    "3.1_por_trimestre": (sql_por_trimestre, "analise_3_1_trimestre.csv"),
    "3.1_por_mes": (sql_por_mes, "analise_3_1_mes.csv"),
    "3.2_por_estabelecimento": (sql_por_estabelecimento, "analise_3_2_estabelecimento_ranking.csv"),
    "3.3_perfil_demografico": (sql_perfil_demografico, "analise_3_3_perfil_demografico.csv"),
    "3.3_top_diagnosticos": (sql_top_diagnosticos, "analise_3_3_top_20_diagnosticos.csv"),
    "3.3_proc_hipertensao": (sql_proc_cronicos_hipertensao, "analise_3_3_procedimentos_hipertensao.csv"),
    "3.4_top_municipios": (sql_fluxo_top_municipios, "analise_3_4_top_30_municipios.csv"),
    "3.4_estab_dependentes": (sql_fluxo_estab_dependentes, "analise_3_4_regioes_dependentes.csv"),
    "3.5_financeiro_total_ijui": (sql_financeiro_total_ijui, "analise_3_5_financeiro_ijui.csv"),
    "3.5_evolucao_gasto_medio": (sql_financeiro_evolucao_media, "analise_3_5_evolucao_gasto_medio.csv"),
    "3.6_foco_oncologia": (sql_foco_oncologia, "analise_3_6_foco_oncologia.csv"),
    "3.6_foco_saude_mental": (sql_foco_saude_mental, "analise_3_6_foco_saude_mental.csv"),
    "3.6_foco_diabetes": (sql_foco_diabetes, "analise_3_6_foco_diabetes.csv"),
    "3.7_comp_regional": (sql_comp_regional, "analise_3_7_comparacao_regional.csv"),
}

# Loop para executar todas as análises padrão
for nome, (sql, csv) in mapa_analises.items():
    executar_e_salvar(nome, sql, csv)

# --- 6. EXECUÇÃO DAS ANÁLISES COM PLOTAGEM ---

# Análise 3.4 (Gráfico de Pizza Ijuí vs. Outros)
print("\n--- Iniciando Análise e Plotagem: 3.4_plot_ijui_vs_outros ---")
try:
    df_ijui_vs_outros = pd.read_sql(sql_fluxo_ijui_vs_outros, engine)
    caminho_arquivo = os.path.join(output_dir, "analise_3_4_ijui_vs_outros.csv")
    df_ijui_vs_outros.to_csv(caminho_arquivo, index=False, sep=';', encoding='utf-8-sig')
    
    # Plotagem
    df_pizza = df_ijui_vs_outros[df_ijui_vs_outros['Origem_Paciente'] != 'Não Informado'].set_index('Origem_Paciente')
    plt.figure(figsize=(10, 7))
    df_pizza['Total_Procedimentos'].plot(kind='pie', autopct='%1.1f%%', startangle=90, fontsize=12, colors=['#66b3ff','#ff9999'])
    plt.title('Proporção de Atendimentos: Moradores de Ijuí vs. Outros Municípios')
    plt.ylabel('')
    caminho_grafico = os.path.join(output_dir, 'grafico_3_4_pizza_fluxo_regional.png')
    plt.savefig(caminho_grafico)
    plt.close() # Fecha a figura para liberar memória
    print(f"    -> Sucesso! Gráfico salvo em: grafico_3_4_pizza_fluxo_regional.png")
except Exception as e:
    print(f"    -> ❌ ERRO ao plotar '3.4_plot_ijui_vs_outros': {e}")

# Análise 3.7 (Gráfico de Tendência Regional)
print("\n--- Iniciando Análise e Plotagem: 3.7_plot_tendencia_regional ---")
try:
    df_tendencia_regional = pd.read_sql(sql_tendencia_demanda_regional, engine)
    caminho_arquivo = os.path.join(output_dir, "analise_3_7_tendencia_demanda_regional.csv")
    df_tendencia_regional.to_csv(caminho_arquivo, index=False, sep=';', encoding='utf-8-sig')

    # Plotagem
    plt.figure(figsize=(12, 7))
    df_pivot_regional = df_tendencia_regional.pivot(index='Mes_Ano', columns='Grupo_Regional', values='Total_Procedimentos')
    df_pivot_regional.plot(kind='line', marker='o', ax=plt.gca())
    plt.title('Tendência de Demanda (Ijuí vs. Outros Municípios)')
    plt.xlabel('Mês'); plt.ylabel('Total de Procedimentos'); plt.legend(title='Grupo Regional'); plt.grid(True); plt.tight_layout()
    caminho_grafico = os.path.join(output_dir, 'grafico_3_7_tendencia_regional.png')
    plt.savefig(caminho_grafico)
    plt.close()
    print(f"    -> Sucesso! Gráfico salvo em: grafico_3_7_tendencia_regional.png")
except Exception as e:
    print(f"    -> ❌ ERRO ao plotar '3.7_plot_tendencia_regional': {e}")

# Análise 3.7 (Gráfico de Tendência Idosos)
print("\n--- Iniciando Análise e Plotagem: 3.7_plot_tendencia_idosos ---")
try:
    df_tendencia_idosos = pd.read_sql(sql_tendencia_idosos_criticos, engine)
    caminho_arquivo = os.path.join(output_dir, "analise_3_7_tendencia_idosos.csv")
    df_tendencia_idosos.to_csv(caminho_arquivo, index=False, sep=';', encoding='utf-8-sig')

    # Plotagem
    plt.figure(figsize=(12, 7))
    df_pivot_idosos = df_tendencia_idosos.pivot(index='Mes_Ano', columns='Area_Critica', values='Total_Procedimentos')
    df_pivot_idosos.plot(kind='line', marker='o', ax=plt.gca())
    plt.title('Tendência de Procedimentos Críticos (Idosos 60+)')
    plt.xlabel('Mês'); plt.ylabel('Total de Procedimentos'); plt.legend(title='Área Crítica'); plt.grid(True); plt.tight_layout()
    caminho_grafico = os.path.join(output_dir, 'grafico_3_7_tendencia_idosos.png')
    plt.savefig(caminho_grafico)
    plt.close()
    print(f"    -> Sucesso! Gráfico salvo em: grafico_3_7_tendencia_idosos.png")
except Exception as e:
    print(f"    -> ❌ ERRO ao plotar '3.7_plot_tendencia_idosos': {e}")

print("\n--- SCRIPT DE RELATÓRIO FINAL CONCLUÍDO! ---")
print(f"Todos os resultados foram salvos na pasta: '{output_dir}'")