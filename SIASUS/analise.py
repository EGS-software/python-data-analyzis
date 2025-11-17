# --- analise.py ---
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
# Importa as variáveis do seu outro arquivo
import queries 

# --- 1. CONFIGURAÇÃO DA CONEXÃO ---

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

# --- 7. EXECUÇÃO DA ANÁLISE 3.6 ---

print("\n--- Análise 3.6: Foco em Oncologia (Top 20 CIDs) ---")
try:
    df_oncologia = pd.read_sql(queries.sql_foco_oncologia, engine)
    print(df_oncologia)
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")


print("\n--- Análise 3.6: Foco em Saúde Mental (Top 20 CIDs) ---")
try:
    df_saude_mental = pd.read_sql(queries.sql_foco_saude_mental, engine)
    print(df_saude_mental)
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")


print("\n--- Análise 3.6: Foco em Atenção Básica (Top Procedimentos Diabetes) ---")
try:
    df_diabetes = pd.read_sql(queries.sql_foco_diabetes, engine)
    print(df_diabetes)
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")

# --- 8. EXECUÇÃO DA ANÁLISE 3.7 ---

print("\n--- Análise 3.7: Comparação Regional (Ijuí, Santa Rosa, Cruz Alta) ---")
try:
    df_comp_regional = pd.read_sql(queries.sql_comp_regional, engine)
    print(df_comp_regional)

    print("\n--- Análise 3.7: Tendência de Demanda (Ijuí vs. Regional) ---")
    try:
        df_tendencia_regional = pd.read_sql(queries.sql_tendencia_demanda_regional, engine)
        print(df_tendencia_regional)

        # --- CÓDIGO DE PLOTAGEM (MATPLOTLIB) ---
        # 1. Prepara o gráfico
        plt.figure(figsize=(12, 7))
        
        # 2. Pivota o DataFrame para plotar as duas linhas (Ijuí e Outros)
        df_pivot_regional = df_tendencia_regional.pivot(
            index='Mes_Ano', 
            columns='Grupo_Regional', 
            values='Total_Procedimentos'
        )
        
        # 3. Plota o gráfico de linhas
        df_pivot_regional.plot(kind='line', marker='o', ax=plt.gca())
        
        # 4. Adiciona títulos e legendas
        plt.title('Tendência de Demanda (Ijuí vs. Outros Municípios)')
        plt.xlabel('Mês')
        plt.ylabel('Total de Procedimentos')
        plt.legend(title='Grupo Regional')
        plt.grid(True)
        plt.tight_layout() # Ajusta o layout
        
        # 5. Salva o gráfico como um arquivo PNG
        plt.savefig('grafico_tendencia_regional.png')
        plt.close() # Fecha a figura para liberar memória
        print(">>> Gráfico 'grafico_tendencia_regional.png' salvo com sucesso.")
        # --- FIM DA PLOTAGEM ---

    except Exception as e:
        print(f"Erro ao executar ou plotar a consulta: {e}")


    print("\n--- Análise 3.7: Tendência de Procedimentos Críticos (Idosos 60+) ---")
    try:
        df_tendencia_idosos = pd.read_sql(queries.sql_tendencia_idosos_criticos, engine)
        print(df_tendencia_idosos)

        # --- CÓDIGO DE PLOTAGEM (MATPLOTLIB) ---
        plt.figure(figsize=(12, 7))
        
        # 2. Pivota o DataFrame (Cardiologia vs. Oncologia)
        df_pivot_idosos = df_tendencia_idosos.pivot(
            index='Mes_Ano', 
            columns='Area_Critica', 
            values='Total_Procedimentos'
        )
        
        # 3. Plota o gráfico de linhas
        df_pivot_idosos.plot(kind='line', marker='o', ax=plt.gca())
        
        # 4. Adiciona títulos e legendas
        plt.title('Tendência de Procedimentos Críticos (Idosos 60+)')
        plt.xlabel('Mês')
        plt.ylabel('Total de Procedimentos')
        plt.legend(title='Área Crítica')
        plt.grid(True)
        plt.tight_layout()
        
        # 5. Salva o gráfico
        plt.savefig('grafico_tendencia_idosos.png')
        plt.close()
        print(">>> Gráfico 'grafico_tendencia_idosos.png' salvo com sucesso.")
        # --- FIM DA PLOTAGEM ---

    except Exception as e:
        print(f"Erro ao executar ou plotar a consulta: {e}")
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")


print("\n--- Análise 3.7: Tendência de Demanda (Ijuí vs. Regional) ---")
try:
    df_tendencia_regional = pd.read_sql(queries.sql_tendencia_demanda_regional, engine)
    print(df_tendencia_regional)
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")


print("\n--- Análise 3.7: Tendência de Procedimentos Críticos (Idosos 60+) ---")
try:
    df_tendencia_idosos = pd.read_sql(queries.sql_tendencia_idosos_criticos, engine)
    print(df_tendencia_idosos)
except Exception as e:
    print(f"Erro ao executar a consulta: {e}")