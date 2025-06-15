import pandas as pd
import os
from phone_utils import padronizar_telefone

# Obtenha o diretório atual do script (mais robusto)
script_dir = os.path.dirname(__file__)

# Construa os caminhos completos para os arquivos
# Ajuste 'Caminho/Completo/Ate/Sua/Pasta/' conforme o local real
caminho_clientes = os.path.join(script_dir, 'clientes.csv')
caminho_report = os.path.join(script_dir, 'meta-ads.xlsx')

# Carregar os dados
df_clientes = pd.read_csv(caminho_clientes)
df_report = pd.read_excel(caminho_report)

# Padronizar telefones dos dois arquivos
df_clientes['telefone_padrao'] = df_clientes['telefone'].apply(padronizar_telefone)
df_report['telefone_padrao'] = df_report['Telefone'].apply(padronizar_telefone)

# Procurar interseção
telefones_report = set(df_report['telefone_padrao'])
repetidos = df_clientes[df_clientes['telefone_padrao'].isin(telefones_report)]

# Mostrar os repetidos (nome e telefone)
print(repetidos[['nome', 'telefone_padrao', 'contrato']])