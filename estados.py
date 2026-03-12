# =================================================================
# VRS Soluções
# JÁ VENDEU? - GESTÃO DE LOCALIDADE (ESTADOS)
# MÓDULO: estados.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================

def obter_estados_vrs():
    """Retorna a lista oficial de estados brasileiros para o sistema."""
    return [
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", 
        "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", 
        "RS", "RO", "RR", "SC", "SP", "SE", "TO"
    ]

def obter_estados_com_todos_vrs():
    """Lista de estados com a opção de filtro geral."""
    lista = ["Todos"]
    lista.extend(obter_estados_vrs())
    return lista