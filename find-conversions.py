import os
import pandas as pd
from utils import padronizar_telefone, parsear_contrato

# Obtenha informações do diretório
script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, 'data', '2025')

# Obter caminhos dos arquivos
caminho_clientes = os.path.join(data_dir, 'clientes.csv')
caminho_report = os.path.join(data_dir, 'meta-ads.xlsx')

# Carregar os dados
df_clientes = pd.read_csv(caminho_clientes)
df_report = pd.read_excel(caminho_report)

# Padronizar telefones dos dois arquivos
df_clientes['telefone_padrao'] = df_clientes['telefone'].apply(padronizar_telefone)
df_report['telefone_padrao'] = df_report['Telefone'].apply(padronizar_telefone)

# Procurar interseção
telefones_report = set(df_report['telefone_padrao'])
repetidos = df_clientes[df_clientes['telefone_padrao'].isin(telefones_report)]

# Parsear a coluna contrato
repetidos['contrato'] = repetidos['contrato'].apply(parsear_contrato)

# Mostrar os repetidos (nome e telefone)
print(repetidos[['nome', 'telefone_padrao', 'contrato']])