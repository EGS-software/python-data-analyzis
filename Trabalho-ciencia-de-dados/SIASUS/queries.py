# --- queries.py ---

# Etapa 3.1: Análise por Trimestre
sql_por_trimestre = """
SELECT
    T.anotri AS "Ano_Trimestre",
    COUNT(*) AS "Total_de_Procedimentos",
    SUM(P.pa_valapr) AS "Valor_Total_Aprovado"
FROM
    pars AS P
JOIN
    DIMTEMPO AS T ON P.pa_cmp = T.anomes
GROUP BY
    T.anotri
ORDER BY
    T.anotri DESC;
"""

# Etapa 3.1: Análise por Mês
sql_por_mes = """
SELECT
    T.MAExt AS "Mes_Ano",
    COUNT(*) AS "Total_de_Procedimentos",
    SUM(P.pa_valapr) AS "Valor_Total_Aprovado"
FROM
    pars AS P
JOIN
    DIMTEMPO AS T ON P.pa_cmp = T.anomes
GROUP BY
    T.MAExt, T.mes
ORDER BY
    T.mes DESC;
"""


# ---
# Etapa 3.2: Produção por Estabelecimento de Saúde
# ---
sql_por_estabelecimento = """
SELECT
    pa_coduni AS "Codigo_Estabelecimento",
    
    -- Total de procedimentos Aprovados vs. Produzidos
    SUM(pa_qtdpro) AS "Total_Qtd_Produzida",
    SUM(pa_qtdapr) AS "Total_Qtd_Aprovada",
    
    -- Taxa de procedimentos produzidos (em porcentagem)
    -- Usamos NULLIF para evitar erro de divisão por zero
    (SUM(pa_qtdpro) / NULLIF(SUM(pa_qtdapr), 0)) * 100 AS "Taxa_Producao_Pct",

    -- Total de valores Aprovados vs. Produzidos
    SUM(pa_valpro) AS "Valor_Total_Produzido",
    SUM(pa_valapr) AS "Valor_Total_Aprovado",
    
    -- Diferença (quanto o hospital produziu a mais ou a menos do que foi aprovado)
    SUM(pa_valpro) - SUM(pa_valapr) AS "Diferenca_Financeira"
FROM
    pars
GROUP BY
    -- Agrupa todos os registros pelo código do estabelecimento
    pa_coduni
ORDER BY
    -- Cria o ranking pelo Valor Total Aprovado (do maior para o menor)
    Valor_Total_Aprovado DESC;
"""

# ---
# Etapa 3.3: Perfil Demográfico (Sexo e Faixa Etária)
# ---
sql_perfil_demografico = """
SELECT
    pa_sexo AS "Sexo",
    
    -- Agrupamento por Faixa Etária
    CASE
        WHEN pa_idade <= 9 THEN '0-9 anos'
        WHEN pa_idade BETWEEN 10 AND 19 THEN '10-19 anos'
        WHEN pa_idade BETWEEN 20 AND 29 THEN '20-29 anos'
        WHEN pa_idade BETWEEN 30 AND 39 THEN '30-39 anos'
        WHEN pa_idade BETWEEN 40 AND 49 THEN '40-49 anos'
        WHEN pa_idade BETWEEN 50 AND 59 THEN '50-59 anos'
        WHEN pa_idade >= 60 THEN '60+ anos'
        ELSE 'Idade Desconhecida'
    END AS "Faixa_Etaria",
    
    COUNT(*) AS "Total_Procedimentos"
FROM
    pars
GROUP BY
    Sexo, Faixa_Etaria
ORDER BY
    Total_Procedimentos DESC;
"""

# ---
# Etapa 3.3: Principais Diagnósticos (CID)
# ---
sql_top_diagnosticos = """
SELECT
    P.pa_cidpri AS "Codigo_CID",
    
    
    S.cd_descr AS "Nome_Diagnostico", 
    
    COUNT(*) AS "Total_Procedimentos"
FROM
    pars AS P
LEFT JOIN
    
    s_cid AS S ON P.pa_cidpri = S.cd_cod
GROUP BY
    P.pa_cidpri, S.cd_descr
ORDER BY
    Total_Procedimentos DESC
LIMIT 20;
"""
# ---
# Etapa 3.3: Procedimentos para Doenças Crônicas (Ex: Hipertensão)
# ---
sql_proc_cronicos = """
SELECT
    pa_proc_id AS "Codigo_Procedimento",
    COUNT(*) AS "Total_Procedimentos"
FROM
    pars
WHERE
    -- Filtra apenas por CIDs de Hipertensão (I10 a I15)
    pa_cidpri BETWEEN 'I10' AND 'I15'
GROUP BY
    pa_proc_id
ORDER BY
    Total_Procedimentos DESC
LIMIT 20; -- 20 procedimentos mais comuns para hipertensão
"""


# ---
#  Etapa 3.4: Fluxos Regionais (Top 30 Municípios de Origem)
# ---
sql_fluxo_estab_dependentes = """
SELECT
    P.pa_coduni AS "Codigo_Estabelecimento",
    P.pa_munpcn AS "Codigo_Municipio_Paciente",
    
    
    M.ds_nome AS "Nome_Municipio_Paciente",
    
    COUNT(*) AS "Total_Procedimentos"
FROM
    pars AS P
LEFT JOIN
    
    tb_municip AS M ON P.pa_munpcn = M.co_municip
WHERE
    -- Filtra APENAS pacientes que NÃO são de Ijuí e NÃO são 'Não Informado'
    P.pa_munpcn != '431490' AND P.pa_munpcn != '999999'
GROUP BY
    P.pa_coduni, P.pa_munpcn, M.ds_nome
ORDER BY
    Total_Procedimentos DESC
LIMIT 50;
"""
# ---
#  Etapa 3.4: Fluxos Regionais (Ijuí vs. Outros)
# ---
sql_fluxo_ijui_vs_outros = """
SELECT
    CASE
        WHEN pa_munpcn = '431490' THEN 'Morador de Ijuí'
        WHEN pa_munpcn = '999999' THEN 'Não Informado'
        WHEN pa_munpcn IS NULL THEN 'Não Informado'
        ELSE 'Morador de Outros Municípios'
    END AS "Origem_Paciente",
    COUNT(*) AS "Total_Procedimentos",
    SUM(pa_valapr) AS "Valor_Total_Aprovado"
FROM
    pars
GROUP BY
    Origem_Paciente
ORDER BY
    Total_Procedimentos DESC;
"""

# ---
# Etapa 3.4: Fluxos Regionais (Regiões Dependentes por Estabelecimento)
# ---
sql_fluxo_estab_dependentes = """
SELECT
    P.pa_coduni AS "Codigo_Estabelecimento", -- Você pode 'traduzir' com a 'cadgerrs' no Pandas
    P.pa_munpcn AS "Codigo_Municipio_Paciente",
    M.no_munic AS "Nome_Municipio_Paciente",
    COUNT(*) AS "Total_Procedimentos"
FROM
    pars AS P
LEFT JOIN
    tb_municip AS M ON P.pa_munpcn = M.co_municdv
WHERE
    -- Filtra APENAS pacientes que NÃO são de Ijuí e NÃO são 'Não Informado'
    P.pa_munpcn != '431490' AND P.pa_munpcn != '999999'
GROUP BY
    P.pa_coduni, P.pa_munpcn, M.no_munic
ORDER BY
    Total_Procedimentos DESC
LIMIT 50; -- Top 50 fluxos "Estabelecimento -> Município Externo"
"""

# ---
# Etapa 3.5: Recursos Financeiros (Total Ijuí vs. Produzido)
# ---
sql_financeiro_total_ijui = """
SELECT
    'Moradores de Ijuí' AS Foco_Analise,
    SUM(pa_valapr) AS "Valor_Total_Aprovado_SUS",
    SUM(pa_valpro) AS "Valor_Total_Produzido",
    
    -- Diferença entre o que foi produzido e o que foi aprovado
    SUM(pa_valpro) - SUM(pa_valapr) AS "Diferenca_Financeira"
FROM
    pars
WHERE
    -- Filtra APENAS por pacientes de Ijuí
    pa_munpcn = '431490'; 
"""

# ---
# Etapa 3.5: Recursos Financeiros (Evolução do Gasto Médio)
# ---
sql_financeiro_evolucao_media = """
SELECT
    T.MAExt AS "Mes_Ano",
    
    -- Calcula o gasto médio APROVADO por procedimento
    AVG(P.pa_valapr) AS "Gasto_Medio_Aprovado",
    
    -- Calcula o gasto médio PRODUZIDO por procedimento
    AVG(P.pa_valpro) AS "Gasto_Medio_Produzido"
FROM
    pars AS P
JOIN
    DIMTEMPO AS T ON P.pa_cmp = T.anomes
GROUP BY
    T.MAExt, T.mes
ORDER BY
    T.mes;
"""

# ---
#  Etapa 3.6: Foco em Áreas Críticas (Oncologia)
# ---
sql_foco_oncologia = """
SELECT
    pa_cidpri AS "Codigo_CID",
    COUNT(*) AS "Total_Procedimentos",
    
    -- Compara os valores aprovados vs. produzidos
    SUM(pa_valapr) AS "Valor_Total_Aprovado",
    SUM(pa_valpro) AS "Valor_Total_Produzido",
    SUM(pa_valpro) - SUM(pa_valapr) AS "Diferenca_Financeira"
FROM
    pars
WHERE
    -- Filtra por todos os CIDs de Oncologia (C00-D48: Neoplasias)
    pa_cidpri BETWEEN 'C00' AND 'D48'
GROUP BY
    pa_cidpri
ORDER BY
    Valor_Total_Aprovado DESC
LIMIT 20; -- Top 20 diagnósticos oncológicos
"""

# ---
#  Etapa 3.6: Foco em Áreas Críticas (Saúde Mental)
# ---
sql_foco_saude_mental = """
SELECT
    pa_cidpri AS "Codigo_CID",
    COUNT(*) AS "Total_Procedimentos",
    SUM(pa_valapr) AS "Valor_Total_Aprovado",
    SUM(pa_valpro) AS "Valor_Total_Produzido",
    SUM(pa_valpro) - SUM(pa_valapr) AS "Diferenca_Financeira"
FROM
    pars
WHERE
    -- Filtra por todos os CIDs de Saúde Mental (F00-F99)
    pa_cidpri BETWEEN 'F00' AND 'F99'
GROUP BY
    pa_cidpri
ORDER BY
    Valor_Total_Aprovado DESC
LIMIT 20; -- Top 20 diagnósticos de saúde mental
"""

# ---
#  Etapa 3.6: Foco em Áreas Críticas (Atenção Básica - Diabetes)
# ---
sql_foco_diabetes = """
SELECT
    pa_proc_id AS "Codigo_Procedimento",
    COUNT(*) AS "Total_Procedimentos",
    SUM(pa_valapr) AS "Valor_Total_Aprovado"
FROM
    pars
WHERE
    -- Filtra por CIDs de Diabetes Mellitus (E10 a E14)
    pa_cidpri BETWEEN 'E10' AND 'E14'
GROUP BY
    pa_proc_id
ORDER BY
    Total_Procedimentos DESC
LIMIT 20; -- Top 20 procedimentos para pacientes com diabetes
"""

# ---
#  Etapa 3.7: Comparações Regionais (Ijuí vs. Santa Rosa vs. Cruz Alta)
# ---
sql_comp_regional = """
SELECT
    CASE
        WHEN pa_munpcn = '431490' THEN 'Ijuí'
        WHEN pa_munpcn = '431720' THEN 'Santa Rosa'
        WHEN pa_munpcn = '430610' THEN 'Cruz Alta'
    END AS "Municipio",
    COUNT(*) AS "Total_Procedimentos",
    SUM(pa_valapr) AS "Valor_Total_Aprovado"
FROM
    pars
WHERE
    -- Filtra apenas pelos 3 municípios de interesse
    pa_munpcn IN ('431490', '431720', '430610')
GROUP BY
    Municipio
ORDER BY
    Valor_Total_Aprovado DESC;
"""

# ---
#  Etapa 3.7: Tendência de Demanda (Ijuí vs. Média Regional)
# ---
sql_tendencia_demanda_regional = """
SELECT
    T.MAExt AS "Mes_Ano",
    CASE
        WHEN P.pa_munpcn = '431490' THEN 'Ijuí'
        ELSE 'Outros Municípios (Regional)'
    END AS "Grupo_Regional",
    COUNT(*) AS "Total_Procedimentos"
FROM
    pars AS P
JOIN
    DIMTEMPO AS T ON P.pa_cmp = T.anomes
WHERE
    P.pa_munpcn != '999999' -- Exclui 'Não Informado' da média
GROUP BY
    T.MAExt, T.mes, Grupo_Regional
ORDER BY
    T.mes, Grupo_Regional;
"""

# ---
#  Etapa 3.7: Tendências de Envelhecimento (Cardio vs. Onco)
# ---
sql_tendencia_idosos_criticos = """
SELECT
    T.MAExt AS "Mes_Ano",
    CASE
        WHEN P.pa_cidpri BETWEEN 'I00' AND 'I99' THEN 'Cardiologia'
        WHEN P.pa_cidpri BETWEEN 'C00' AND 'D48' THEN 'Oncologia'
    END AS "Area_Critica",
    COUNT(*) AS "Total_Procedimentos"
FROM
    pars AS P
JOIN
    DIMTEMPO AS T ON P.pa_cmp = T.anomes
WHERE
    -- Filtra apenas por pacientes com 60 anos ou mais
    P.pa_idade >= 60
    -- Filtra apenas por CIDs Cardiológicos OU Oncológicos
    AND (
        (P.pa_cidpri BETWEEN 'I00' AND 'I99') OR
        (P.pa_cidpri BETWEEN 'C00' AND 'D48')
    )
GROUP BY
    T.MAExt, T.mes, Area_Critica
ORDER BY
    T.mes, Area_Critica;
"""