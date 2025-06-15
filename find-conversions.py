import pandas as pd
import re
import os

# Obtenha o diretório atual do script (mais robusto)
script_dir = os.path.dirname(__file__)

# Construa os caminhos completos para os arquivos
# Ajuste 'Caminho/Completo/Ate/Sua/Pasta/' conforme o local real
caminho_clientes = os.path.join(script_dir, 'clientes.csv')
caminho_report = os.path.join(script_dir, 'meta-ads.xlsx')

# Carregar os dados
df_clientes = pd.read_csv(caminho_clientes)
df_report = pd.read_excel(caminho_report)

# Função para padronizar telefones para o formato: 5512XXXXXXXXX
def padronizar_telefone(telefone):
    # Remove tudo que não for número
    telefone = re.sub(r'\D', '', str(telefone))
    # Se começar com 0, remove
    if telefone.startswith('0'):
        telefone = telefone[1:]
    # Se já começa com 55 e tem 13 dígitos, retorna
    if telefone.startswith('55') and len(telefone) >= 12:
        return telefone[:13]
    # Se tem DDD e número, mas sem 55
    if len(telefone) == 11:
        return '55' + telefone
    # Se tem DDD entre parênteses
    if len(telefone) == 10:
        return '55' + telefone
    # Se já está no formato correto
    if len(telefone) == 13 and telefone.startswith('55'):
        return telefone
    # Se não encaixa, retorna o que tem
    return telefone

# Padronizar telefones dos dois arquivos
df_clientes['telefone_padrao'] = df_clientes['telefone'].apply(padronizar_telefone)
df_report['telefone_padrao'] = df_report['Telefone'].apply(padronizar_telefone)

# Procurar interseção
telefones_report = set(df_report['telefone_padrao'])
repetidos = df_clientes[df_clientes['telefone_padrao'].isin(telefones_report)]

# Mostrar os repetidos (nome e telefone)
print(repetidos[['nome', 'telefone_padrao', 'contrato']])