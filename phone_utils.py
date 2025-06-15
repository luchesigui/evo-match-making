import re

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