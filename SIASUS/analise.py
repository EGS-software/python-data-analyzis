# --- analise.py ---

import pandas as pd
from sqlalchemy import create_engine
# Importa as variáveis do seu outro arquivo
import queries 

# --- 1. CONFIGURAÇÃO DA CONEXÃO ---
# (Faça isso apenas uma vez no topo do seu script)
try:
    # Substitua 'root' e 'SEU_PASSWORD' pelo seu usuário e senha
    engine = create_engine("mysql+mysqlconnector://root:SEU_PASSWORD@localhost:3306/siasus")
    print("Conexão com o banco 'siasus' realizada com sucesso!")
except Exception as e:
    print(f"Erro ao conectar ao MySQL: {e}")
    exit()


# --- 2. EXECUÇÃO DAS ANÁLISES ---

print("\n--- Análise por Trimestre (Etapa 3.1) ---")
try:
    # Usa a query importada do arquivo 'queries.py'
    df_trimestre = pd.read_sql(queries.sql_por_trimestre, engine)
    print(df_trimestre)
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")


print("\n--- Análise por Mês (Etapa 3.1) ---")
try:
    # Usa a segunda query importada
    df_mes = pd.read_sql(queries.sql_por_mes, engine)
    print(df_mes)
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")


# --- 3. EXECUÇÃO DA ANÁLISE 3.2 ---

print("\n--- Análise por Estabelecimento (Etapa 3.2) ---")
try:
    # Usa a nova query importada
    df_estab = pd.read_sql(queries.sql_por_estabelecimento, engine)
    
    print("Ranking de Produção por Estabelecimento:")
    print(df_estab)

    
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")


# --- 4. EXECUÇÃO DA ANÁLISE 3.3 ---

print("\n--- Análise 3.3: Perfil Demográfico (Sexo e Faixa Etária) ---")
try:
    df_demo = pd.read_sql(queries.sql_perfil_demografico, engine)
    print(df_demo)
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")


print("\n--- Análise 3.3: Top 20 Diagnósticos (CID) ---")
try:
    df_cid = pd.read_sql(queries.sql_top_diagnosticos, engine)
    print(df_cid)
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")


print("\n--- Análise 3.3: Top Procedimentos (Hipertensão) ---")
try:
    df_cronicos = pd.read_sql(queries.sql_proc_cronicos, engine)
    print(df_cronicos)
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")

# --- 5. EXECUÇÃO DA ANÁLISE 3.4 ---

print("\n--- Análise 3.4: Top 30 Municípios de Origem ---")
try:
    df_top_mun = pd.read_sql(queries.sql_fluxo_top_municipios, engine)
    print(df_top_mun)
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")


print("\n--- Análise 3.4: Atendimentos (Ijuí vs. Outros) ---")
try:
    df_ijui_vs_outros = pd.read_sql(queries.sql_fluxo_ijui_vs_outros, engine)
    print(df_ijui_vs_outros)
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")


print("\n--- Análise 3.4: Top 50 Regiões Dependentes por Estabelecimento ---")
try:
    df_dependentes = pd.read_sql(queries.sql_fluxo_estab_dependentes, engine)
    print(df_dependentes)
    # df_dependentes.to_excel("fluxo_estabelecimentos_externos.xlsx")
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")

# --- 6. EXECUÇÃO DA ANÁLISE 3.5 ---

print("\n--- Análise 3.5: Recursos Financeiros (Total Ijuí) ---")
try:
    df_financeiro_total = pd.read_sql(queries.sql_financeiro_total_ijui, engine)
    print(df_financeiro_total)
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")


print("\n--- Análise 3.5: Evolução do Gasto Médio por Procedimento ---")
try:
    df_financeiro_evolucao = pd.read_sql(queries.sql_financeiro_evolucao_media, engine)
    print(df_financeiro_evolucao)
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")