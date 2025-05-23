import pandas as pd
import os

# Caminho da pasta com os arquivos
caminho_pasta = '../Dados/Censo Escolar/'

# Lista com os arquivos a serem processados
arquivos = [
    'microdados_ed_basica_2013.csv',
    'microdados_ed_basica_2015.csv',
    'microdados_ed_basica_2017.csv',
    'microdados_ed_basica_2019.csv',
    'microdados_ed_basica_2021.csv',
    'microdados_ed_basica_2023.csv',
]

# Colunas que queremos extrair
colunas_utilizadas = [
    'NU_ANO_CENSO', 'CO_ENTIDADE', 'NO_ENTIDADE',
    'SG_UF', 'CO_MUNICIPIO', 'NO_MUNICIPIO',
    'TP_DEPENDENCIA', 'TP_LOCALIZACAO',
    'IN_BIBLIOTECA', 'IN_LABORATORIO_INFORMATICA', 'IN_INTERNET', 'IN_ENERGIA_REDE_PUBLICA'
]

# Lista para armazenar os DataFrames processados
lista_dfs = []

# Ler cada arquivo e extrair colunas
for arquivo in arquivos:
    print(f'📂 Lendo {arquivo}...')
    caminho = os.path.join(caminho_pasta, arquivo)
    df = pd.read_csv(caminho, sep=';', encoding='latin1', usecols=lambda col: col in colunas_utilizadas)
    lista_dfs.append(df)

# Concatenar todos os anos
df_censo = pd.concat(lista_dfs, ignore_index=True)

# Salvar em um único arquivo CSV
df_censo.to_csv('../Dados/censo_escolar_2013_2023.csv', index=False, sep=';', encoding='utf-8')

# Visualizar as primeiras linhas
print(df_censo.head(10))
