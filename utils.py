import re
import pandas as pd

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

def parsear_contrato(contrato):
    # Se for NaN, retorna o texto padrão
    if pd.isna(contrato):
        return "FREEPASS - NÃO RENOVADO"
    
    # Converte para string
    contrato = str(contrato)
    
    # Remove pontuação
    contrato = contrato.replace('.', '')
    
    # Remove texto entre parênteses
    contrato = re.sub(r'\([^)]*\)', '', contrato)
    
    # Remove espaços extras e retorna
    return contrato.strip()

def mostrar_metricas_conversao(df_clientes, df_report, df_repetidos):
    total_clientes = len(df_clientes)
    total_oportunidades = len(df_report)
    
    # Conta conversões excluindo FREEPASS
    conversoes = df_repetidos[~df_repetidos['contrato'].str.contains('FREEPASS', case=False, na=False)]
    total_conversoes = len(conversoes)
    
    # Calcula taxa de conversão
    taxa_conversao = (total_conversoes / total_oportunidades) * 100 if total_oportunidades > 0 else 0
    
    print(f"Total de clientes: {total_clientes}")
    print(f"Total de oportunidades: {total_oportunidades}")
    print(f"Total de conversões: {total_conversoes}")
    print(f"Taxa de conversão: {taxa_conversao:.2f}%") 