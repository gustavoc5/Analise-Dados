import pandas as pd

# Função para processar qualquer arquivo do IDEB
def processar_ideb(arquivo, etapa):
    df = pd.read_excel(arquivo, skiprows=3)

    df.rename(columns={
        'Sigla da UF': 'SG_UF',
        'Código do Município': 'CO_MUNICIPIO',
        'Nome do Município': 'NO_MUNICIPIO',
        'Código da Escola': 'ID_ESCOLA',
        'Nome da Escola': 'NO_ESCOLA',
        'Rede': 'REDE'
    }, inplace=True)

    # Definir colunas por etapa
    if etapa == 'EM':
        anos_validos = ['2017', '2019', '2021', '2023']
    else:
        anos_validos = ['2013', '2015', '2017', '2019', '2021', '2023']
    
    colunas_ideb = [f'VL_OBSERVADO_{ano}' for ano in anos_validos if f'VL_OBSERVADO_{ano}' in df.columns]

    df_long = pd.melt(
        df,
        id_vars=['ID_ESCOLA', 'NO_ESCOLA', 'REDE', 'SG_UF', 'CO_MUNICIPIO', 'NO_MUNICIPIO'],
        value_vars=colunas_ideb,
        var_name='VARIAVEL_ANO',
        value_name='IDEB'
    )

    df_long['ANO'] = df_long['VARIAVEL_ANO'].str.extract(r'(\d{4})').astype(int)
    df_long.drop(columns='VARIAVEL_ANO', inplace=True)
    df_long['ETAPA'] = etapa
    df_final = df_long[['ID_ESCOLA', 'NO_ESCOLA', 'REDE', 'SG_UF',
                        'CO_MUNICIPIO', 'NO_MUNICIPIO', 'ANO', 'ETAPA', 'IDEB']]
    df_final.sort_values(by=['ID_ESCOLA', 'ANO'], inplace=True)
    df_final['IDEB'] = pd.to_numeric(df_final['IDEB'], errors='coerce')
    
    return df_final

# Processar cada etapa
df_ai = processar_ideb('../Dados/IDEB/divulgacao_anos_iniciais_escolas_2005-2023.xlsx', 'AI')
df_af = processar_ideb('../Dados/IDEB/divulgacao_anos_finais_escolas_2005-2023.xlsx', 'AF')
df_em = processar_ideb('../Dados/IDEB/divulgacao_ensino_medio_escolas_2005-2023.xlsx', 'EM')

# Concatenar todos
df_ideb_completo = pd.concat([df_ai, df_af, df_em], ignore_index=True)
df_ideb_completo.sort_values(by=['ID_ESCOLA', 'ANO'], inplace=True)

# Salvar o resultado
df_ideb_completo.to_csv('../Dados/IDEB/ideb_2013_2023_formatado.csv', index=False, encoding='utf-8-sig')

# Exibir amostra
print(df_ideb_completo.head(10))
