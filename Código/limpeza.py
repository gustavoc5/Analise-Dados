import pandas as pd

# Leitura dos arquivos
censo = pd.read_csv('../Dados/Censo Escolar/censo_escolar_2013_2023.csv', encoding='latin1', sep=';', low_memory=False)
ideb = pd.read_csv('../Dados/IDEB/ideb_2013_2023_formatado.csv', encoding='latin1', sep=',', low_memory=False)

# Normalização dos nomes das colunas
censo.columns = censo.columns.str.strip().str.upper()
ideb.columns = ideb.columns.str.strip().str.upper()

# Renomear SG_UF do Censo para evitar conflito no merge
censo.rename(columns={'SG_UF': 'UF_CENSO'}, inplace=True)

# Converter ID da escola para string sem decimal
ideb['ID_ESCOLA'] = ideb['ID_ESCOLA'].astype(str).str.split('.').str[0]
censo['CO_ENTIDADE'] = censo['CO_ENTIDADE'].astype(str)

# Remover ausentes e converter ANO para int
ideb = ideb.dropna(subset=['ANO', 'IDEB'])
ideb['ANO'] = ideb['ANO'].astype(int)

# Converter NU_ANO_CENSO para int
censo['NU_ANO_CENSO'] = censo['NU_ANO_CENSO'].astype(int)

# Remover notas IDEB inválidas (<= 0)
ideb = ideb[ideb['IDEB'] > 0]

# Realizar o merge
dados = pd.merge(
    ideb,
    censo,
    left_on=['ID_ESCOLA', 'ANO'],
    right_on=['CO_ENTIDADE', 'NU_ANO_CENSO'],
    how='inner'
)

# Converter infraestrutura para int
infra_cols = ['IN_BIBLIOTECA', 'IN_LABORATORIO_INFORMATICA', 'IN_INTERNET', 'IN_ENERGIA_REDE_PUBLICA']
dados[infra_cols] = dados[infra_cols].fillna(0).astype(int)

# Mapear valores legíveis
map_dep = {1: 'Federal', 2: 'Estadual', 3: 'Municipal', 4: 'Privada'}
map_loc = {1: 'Urbana', 2: 'Rural'}

dados['DEPENDENCIA'] = dados['TP_DEPENDENCIA'].map(map_dep)
dados['LOCALIZACAO'] = dados['TP_LOCALIZACAO'].map(map_loc)

# Selecionar colunas finais (com UF do Censo renomeada)
colunas_finais = [
    'CO_ENTIDADE', 'ANO', 'UF_CENSO', 'ETAPA', 'IDEB',
    'DEPENDENCIA', 'LOCALIZACAO',
    'IN_BIBLIOTECA', 'IN_LABORATORIO_INFORMATICA',
    'IN_INTERNET', 'IN_ENERGIA_REDE_PUBLICA'
]

dados_final = dados[colunas_finais]

# Exportar o resultado
dados_final.to_csv('../Dados/dados_integrados.csv', index=False)
