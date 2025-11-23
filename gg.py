import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import os
import sys

print("--- INICIANDO RELATÓRIO FINAL (v17 - CORREÇÃO PLOTAGEM) ---")
print("Filtro: Produção de Ijuí (431020)")
print("Faixas: Criança(5-13), Adolescente(14-17), Adulto(18-59), Idoso(60+)")

# --- 1. CONFIGURAÇÃO DA CONEXÃO ---
try:
    # ⚠️ DIGITE SUA SENHA DO MYSQL AQUI ABAIXO ⚠️
    engine = create_engine("mysql+mysqlconnector://root:Tiag123!@localhost:3306/siasus")
    
    # Teste de conexão inicial
    with engine.connect() as conexao:
        print("\n✅ Conexão com o banco 'siasus' realizada com sucesso!")
except Exception as e:
    print(f"\n❌ Erro fatal ao conectar ao MySQL: {e}")
    print("--- \nPOR FAVOR, VERIFIQUE SUA SENHA NA LINHA create_engine() ---")
    sys.exit()

# --- 2. DEFINIÇÃO DAS QUERIES ---

# Etapa 3.1
sql_por_trimestre = """
SELECT T.anotri AS "Ano_Trimestre", COUNT(*) AS "Total_de_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual",
    SUM(P.pa_valapr) AS "Valor_Total_Aprovado"
FROM pars AS P JOIN DIMTEMPO AS T ON P.pa_cmp = T.anomes
WHERE P.pa_ufmun = '431020'
GROUP BY T.anotri ORDER BY T.anotri DESC;
"""
sql_por_mes = """
SELECT T.MAExt AS "Mes_Ano", COUNT(*) AS "Total_de_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual",
    SUM(P.pa_valapr) AS "Valor_Total_Aprovado"
FROM pars AS P JOIN DIMTEMPO AS T ON P.pa_cmp = T.anomes
WHERE P.pa_ufmun = '431020'
GROUP BY T.MAExt, T.mes ORDER BY T.mes DESC;
"""

# Etapa 3.2
sql_por_estabelecimento = """
SELECT
    P.pa_coduni AS "Codigo_Estabelecimento",
    E.fantasia AS "Nome_Estabelecimento", 
    COUNT(*) AS "Total_Atendimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Pct_Atendimentos_Total",
    SUM(P.pa_valapr) AS "Valor_Total_Aprovado"
FROM pars AS P
LEFT JOIN CADGERRS AS E ON P.pa_coduni = E.cnes
WHERE P.pa_ufmun = '431020'
GROUP BY P.pa_coduni, E.fantasia
ORDER BY Total_Atendimentos DESC;
"""

# Etapa 3.3: Faixa Etária (Consolidada)
sql_faixa_etaria_isolada = """
SELECT
    CASE
        WHEN CAST(pa_idade AS UNSIGNED) < 5 THEN '00-04 Anos'
        WHEN CAST(pa_idade AS UNSIGNED) BETWEEN 5 AND 13 THEN 'Criança (5-13)'
        WHEN CAST(pa_idade AS UNSIGNED) BETWEEN 14 AND 17 THEN 'Adolescente (14-17)'
        WHEN CAST(pa_idade AS UNSIGNED) BETWEEN 18 AND 59 THEN 'Adulto (18-59)'
        WHEN CAST(pa_idade AS UNSIGNED) >= 60 THEN 'Idoso (60+)'
        ELSE 'Idade Não Informada'
    END AS "Faixa_Etaria_Resumo",
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual"
FROM pars
WHERE pa_ufmun = '431020'
GROUP BY Faixa_Etaria_Resumo 
ORDER BY Total_Procedimentos DESC;
"""

# Etapa 3.3: Perfil Demográfico
sql_perfil_demografico = """
SELECT
    pa_sexo AS "Sexo",
    CASE
        WHEN CAST(pa_idade AS UNSIGNED) < 5 THEN '00-04 Anos'
        WHEN CAST(pa_idade AS UNSIGNED) BETWEEN 5 AND 13 THEN 'Criança (5-13)'
        WHEN CAST(pa_idade AS UNSIGNED) BETWEEN 14 AND 17 THEN 'Adolescente (14-17)'
        WHEN CAST(pa_idade AS UNSIGNED) BETWEEN 18 AND 59 THEN 'Adulto (18-59)'
        WHEN CAST(pa_idade AS UNSIGNED) >= 60 THEN 'Idoso (60+)'
        ELSE 'Idade Não Informada'
    END AS "Faixa_Etaria_Resumo",
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual"
FROM pars
WHERE pa_ufmun = '431020'
GROUP BY Sexo, Faixa_Etaria_Resumo 
ORDER BY Total_Procedimentos DESC;
"""

# Etapa 3.3: Top Diagnósticos
sql_top_diagnosticos = """
SELECT
    P.pa_cidpri AS "Codigo_CID", S.cd_descr AS "Nome_Diagnostico", 
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual"
FROM pars AS P
LEFT JOIN s_cid AS S ON P.pa_cidpri = S.cd_cod
WHERE P.pa_ufmun = '431020'
GROUP BY P.pa_cidpri, S.cd_descr
ORDER BY Total_Procedimentos DESC LIMIT 20;
"""

# Etapa 3.3: Procedimentos Hipertensão
sql_proc_cronicos_hipertensao = """
SELECT
    P.pa_proc_id AS "Codigo_Procedimento",
    T.ip_dscr AS "Nome_Procedimento",
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual_do_Filtro"
FROM pars AS P
LEFT JOIN TB_SIGTAW AS T ON P.pa_proc_id = T.ip_cod
WHERE P.pa_ufmun = '431020'
  AND (T.ip_dscr LIKE '%HIPERTEN%' OR T.ip_dscr LIKE '%PRESSAO ARTERIAL%')
GROUP BY P.pa_proc_id, T.ip_dscr
ORDER BY Total_Procedimentos DESC LIMIT 20;
"""

# Etapa 3.4: Origem dos Pacientes
sql_fluxo_top_municipios = """
SELECT
    P.pa_munpcn AS "Codigo_Municipio_Origem", M.ds_nome AS "Nome_Municipio_Origem", 
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual"
FROM pars AS P
LEFT JOIN tb_municip AS M ON P.pa_munpcn = M.co_municip
WHERE P.pa_ufmun = '431020'
GROUP BY P.pa_munpcn, M.ds_nome
ORDER BY Total_Procedimentos DESC LIMIT 30;
"""

# Etapa 3.4: Proporção Ijuí vs Outros
sql_fluxo_ijui_vs_outros = """
SELECT
    CASE
        WHEN pa_munpcn = '431020' THEN 'Paciente de Ijuí'
        WHEN pa_munpcn = '999999' THEN 'Origem Não Informada'
        WHEN pa_munpcn IS NULL THEN 'Origem Não Informada'
        ELSE 'Paciente de Outro Município'
    END AS "Origem_Paciente",
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual",
    SUM(pa_valapr) AS "Valor_Total_Aprovado"
FROM pars AS P
WHERE P.pa_ufmun = '431020'
GROUP BY Origem_Paciente ORDER BY Total_Procedimentos DESC;
"""

# Etapa 3.4: Fluxo para Estabelecimentos
sql_fluxo_estab_dependentes = """
SELECT
    E.fantasia AS "Nome_Estabelecimento",
    M.ds_nome AS "Municipio_Origem_Paciente",
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual_do_Filtro"
FROM pars AS P
LEFT JOIN tb_municip AS M ON P.pa_munpcn = M.co_municip
LEFT JOIN CADGERRS AS E ON P.pa_coduni = E.cnes
WHERE P.pa_ufmun = '431020'
  AND P.pa_munpcn != '431020'
  AND P.pa_munpcn != '999999'
GROUP BY E.fantasia, M.ds_nome
ORDER BY Total_Procedimentos DESC LIMIT 50;
"""

# Etapa 3.5: Financeiro Total
sql_financeiro_total = """
SELECT
    'Produção Total de Ijuí' AS Foco_Analise,
    SUM(pa_valapr) AS "Valor_Total_Aprovado_SUS",
    SUM(pa_valpro) AS "Valor_Total_Produzido",
    SUM(pa_valpro) - SUM(pa_valapr) AS "Diferenca_Financeira"
FROM pars
WHERE pa_ufmun = '431020';
"""

# Etapa 3.5: Evolução Gasto Médio
sql_financeiro_evolucao_media = """
SELECT
    T.MAExt AS "Mes_Ano",
    AVG(P.pa_valapr) AS "Gasto_Medio_Aprovado",
    AVG(P.pa_valpro) AS "Gasto_Medio_Produzido"
FROM pars AS P
JOIN DIMTEMPO AS T ON P.pa_cmp = T.anomes
WHERE P.pa_ufmun = '431020'
GROUP BY T.MAExt, T.mes ORDER BY T.mes;
"""

# Etapa 3.6: Oncologia
sql_foco_oncologia = """
SELECT
    S.cd_descr AS "Nome_Diagnostico",
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual_do_Filtro",
    SUM(P.pa_valapr) AS "Valor_Total_Aprovado"
FROM pars AS P
LEFT JOIN s_cid AS S ON P.pa_cidpri = S.cd_cod
LEFT JOIN TB_SIGTAW AS T ON P.pa_proc_id = T.ip_cod
WHERE P.pa_ufmun = '431020'
  AND (P.pa_cidpri BETWEEN 'C00' AND 'D48' OR T.ip_dscr LIKE '%QUIMIOTERAPIA%' OR T.ip_dscr LIKE '%RADIOTERAPIA%')
GROUP BY S.cd_descr
ORDER BY Valor_Total_Aprovado DESC LIMIT 20;
"""

# Etapa 3.6: Saúde Mental
sql_foco_saude_mental = """
SELECT
    S.cd_descr AS "Nome_Diagnostico",
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual_do_Filtro",
    SUM(P.pa_valapr) AS "Valor_Total_Aprovado"
FROM pars AS P
LEFT JOIN s_cid AS S ON P.pa_cidpri = S.cd_cod
LEFT JOIN TB_SIGTAW AS T ON P.pa_proc_id = T.ip_cod
WHERE P.pa_ufmun = '431020'
  AND (P.pa_cidpri BETWEEN 'F00' AND 'F99' OR T.ip_dscr LIKE '%PSICOTERAPIA%' OR T.ip_dscr LIKE '%PSIQUIATR%')
GROUP BY S.cd_descr
ORDER BY Valor_Total_Aprovado DESC LIMIT 20;
"""

# Etapa 3.6: Diabetes
sql_foco_diabetes = """
SELECT
    T.ip_dscr AS "Nome_Procedimento",
    COUNT(*) AS "Total_Procedimentos",
    ROUND((COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()), 2) AS "Percentual_do_Filtro",
    SUM(P.pa_valapr) AS "Valor_Total_Aprovado"
FROM pars AS P
LEFT JOIN TB_SIGTAW AS T ON P.pa_proc_id = T.ip_cod
WHERE P.pa_ufmun = '431020'
  AND (T.ip_dscr LIKE '%DIABET%' OR T.ip_dscr LIKE '%GLICEMIA%' OR T.ip_dscr LIKE '%INSULINA%')
GROUP BY T.ip_dscr
ORDER BY Total_Procedimentos DESC LIMIT 20;
"""

# Etapa 3.7: Comparação Regional
sql_comp_regional = """
SELECT
    CASE
        WHEN pa_ufmun = '431020' THEN 'Ijuí'
        WHEN pa_ufmun = '431720' THEN 'Santa Rosa'
        WHEN pa_ufmun = '430610' THEN 'Cruz Alta'
    END AS "Municipio_Producao",
    COUNT(*) AS "Total_Procedimentos",
    SUM(pa_valapr) AS "Valor_Total_Aprovado"
FROM pars
WHERE pa_ufmun IN ('431020', '431720', '430610')
GROUP BY Municipio_Producao
ORDER BY Valor_Total_Aprovado DESC;
"""

# Etapa 3.7: Tendência Demanda Total
sql_tendencia_demanda = """
SELECT
    T.MAExt AS "Mes_Ano",
    COUNT(*) AS "Total_Procedimentos_Ijui"
FROM pars AS P
JOIN DIMTEMPO AS T ON P.pa_cmp = T.anomes
WHERE P.pa_ufmun = '431020'
GROUP BY T.MAExt, T.mes ORDER BY T.mes;
"""

# Etapa 3.7: Tendência Idosos
sql_tendencia_idosos = """
SELECT
    T.MAExt AS "Mes_Ano",
    CASE
        WHEN P.pa_cidpri BETWEEN 'I00' AND 'I99' THEN 'Cardiologia'
        WHEN P.pa_cidpri BETWEEN 'C00' AND 'D48' THEN 'Oncologia'
    END AS "Area_Critica",
    COUNT(*) AS "Total_Procedimentos"
FROM pars AS P
JOIN DIMTEMPO AS T ON P.pa_cmp = T.anomes
WHERE CAST(P.pa_idade AS UNSIGNED) >= 60
  AND P.pa_ufmun = '431020'
  AND ((P.pa_cidpri BETWEEN 'I00' AND 'I99') OR (P.pa_cidpri BETWEEN 'C00' AND 'D48'))
GROUP BY T.MAExt, T.mes, Area_Critica ORDER BY T.mes, Area_Critica;
"""

# --- 3. EXECUÇÃO E SALVAMENTO ---
output_dir = "resultados_analise_IJUI_FINAL"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
print(f"\nResultados serão salvos em: '{output_dir}'")

mapa_analises = {
    "3.1_trimestre": (sql_por_trimestre, "analise_3_1_trimestre.csv"),
    "3.1_mes": (sql_por_mes, "analise_3_1_mes.csv"),
    "3.2_estabelecimentos": (sql_por_estabelecimento, "analise_3_2_estabelecimentos.csv"),
    "3.3_faixa_etaria": (sql_faixa_etaria_isolada, "analise_3_3_faixa_etaria.csv"), 
    "3.3_demografico": (sql_perfil_demografico, "analise_3_3_demografico_sexo_idade.csv"),
    "3.3_diagnosticos": (sql_top_diagnosticos, "analise_3_3_diagnosticos.csv"),
    "3.3_hipertensao": (sql_proc_cronicos_hipertensao, "analise_3_3_hipertensao.csv"),
    "3.4_origem_pacientes": (sql_fluxo_top_municipios, "analise_3_4_origem_pacientes.csv"),
    "3.4_ijui_vs_outros": (sql_fluxo_ijui_vs_outros, "analise_3_4_ijui_vs_outros.csv"),
    "3.4_fluxo_externo": (sql_fluxo_estab_dependentes, "analise_3_4_fluxo_externo.csv"),
    "3.5_financeiro": (sql_financeiro_total, "analise_3_5_financeiro.csv"),
    "3.5_gasto_medio": (sql_financeiro_evolucao_media, "analise_3_5_gasto_medio.csv"),
    "3.6_oncologia": (sql_foco_oncologia, "analise_3_6_oncologia.csv"),
    "3.6_saude_mental": (sql_foco_saude_mental, "analise_3_6_saude_mental.csv"),
    "3.6_diabetes": (sql_foco_diabetes, "analise_3_6_diabetes.csv"),
    "3.7_comparacao_regional": (sql_comp_regional, "analise_3_7_comparacao_regional.csv"),
}

# Função para executar query com NOVA conexão a cada vez (BLINDAGEM)
def executar_seguro(nome, query, arquivo):
    print(f"\n--- Análise: {nome} ---")
    try:
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
            print(df.head(3))
            df.to_csv(os.path.join(output_dir, arquivo), index=False, sep=';', encoding='utf-8-sig')
            print(f"-> Salvo: {arquivo}")
            return df
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return None

# Loop de Execução
for nome, (sql, csv) in mapa_analises.items():
    executar_seguro(nome, sql, csv)

# --- 4. PLOTAGEM ---
print("\n--- Gerando Gráficos ---")

# Gráfico Faixa Etária
try:
    with engine.connect() as conn:
        df = pd.read_sql(sql_faixa_etaria_isolada, conn)
    if not df.empty:
        plt.figure(figsize=(10, 6))
        # Ordena o índice para ficar na ordem lógica de idade
        ordem_idades = [
            '00-04 Anos', 'Criança (5-13)', 'Adolescente (14-17)', 
            'Adulto (18-59)', 'Idoso (60+)', 'Idade Não Informada'
        ]
        # Filtra apenas o que existe no dataframe
        ordem_existente = [x for x in ordem_idades if x in df['Faixa_Etaria_Resumo'].values]
        
        df.set_index('Faixa_Etaria_Resumo').reindex(ordem_existente).plot(kind='bar', color='skyblue', edgecolor='black', legend=False)
        plt.title('Distribuição de Procedimentos por Faixa Etária (Ijuí)')
        plt.xlabel('Faixa Etária'); plt.ylabel('Volume de Procedimentos')
        plt.xticks(rotation=45); plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'grafico_faixa_etaria.png'))
        plt.close()
        print("-> Gráfico Salvo: grafico_faixa_etaria.png")
except Exception as e: print(f"Erro no gráfico de faixa etária: {e}")

# Gráfico Pizza Origem (QUERY CORRIGIDA)
try:
    # QUERY CORRIGIDA AQUI TAMBÉM (FROM pars AS P)
    sql_pizza_corrigido = """
    SELECT CASE WHEN pa_munpcn = '431020' THEN 'Paciente de Ijuí'
           WHEN pa_munpcn = '999999' THEN 'Origem Não Informada'
           WHEN pa_munpcn IS NULL THEN 'Origem Não Informada'
           ELSE 'Paciente de Outro Município' END AS "Origem_Paciente",
           COUNT(*) AS "Total_Procedimentos"
    FROM pars AS P WHERE P.pa_ufmun = '431020'
    GROUP BY Origem_Paciente ORDER BY Total_Procedimentos DESC;
    """
    with engine.connect() as conn:
        df = pd.read_sql(sql_pizza_corrigido, conn)
    
    if not df.empty and 'Origem_Paciente' in df.columns:
        df_pizza = df[df['Origem_Paciente'] != 'Origem Não Informada'].set_index('Origem_Paciente')
        plt.figure(figsize=(10, 7))
        df_pizza['Total_Procedimentos'].plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#66b3ff','#ff9999'])
        plt.title('Origem dos Pacientes Atendidos em Ijuí')
        plt.ylabel('')
        plt.savefig(os.path.join(output_dir, 'grafico_origem_pacientes.png'))
        plt.close()
        print("-> Gráfico Salvo: grafico_origem_pacientes.png")
except Exception as e: print(f"Erro no gráfico de pizza: {e}")

# Gráfico Tendência Demanda
try:
    with engine.connect() as conn:
        df = pd.read_sql(sql_tendencia_demanda, conn)
    if not df.empty:
        plt.figure(figsize=(12, 7))
        df.set_index('Mes_Ano')['Total_Procedimentos_Ijui'].plot(kind='line', marker='o')
        plt.title('Evolução da Produção Ambulatorial de Ijuí')
        plt.grid(True); plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'grafico_tendencia_demanda.png'))
        plt.close()
        print("-> Gráfico Salvo: grafico_tendencia_demanda.png")
except Exception as e: print(f"Erro no gráfico de demanda: {e}")

# Gráfico Tendência Idosos
try:
    with engine.connect() as conn:
        df = pd.read_sql(sql_tendencia_idosos, conn)
    if not df.empty:
        plt.figure(figsize=(12, 7))
        df_pivot = df.pivot(index='Mes_Ano', columns='Area_Critica', values='Total_Procedimentos')
        df_pivot.plot(kind='line', marker='o', ax=plt.gca())
        plt.title('Tendência Crítica em Idosos (Ijuí)')
        plt.grid(True); plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'grafico_tendencia_idosos.png'))
        plt.close()
        print("-> Gráfico Salvo: grafico_tendencia_idosos.png")
except Exception as e: print(f"Erro no gráfico de idosos: {e}")

print("\n--- SCRIPT FINALIZADO COM SUCESSO! ---")