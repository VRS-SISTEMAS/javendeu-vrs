# =================================================================
# VRS Soluções
# JÁ VENDEU? - GESTÃO DE CATEGORIAS
# MÓDULO: categorias.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================

def obter_categorias_vrs():
    """Retorna a lista oficial de categorias do sistema VRS Soluções."""
    return [
        "Todas", 
        "🚗 Veículos", 
        "📱 Eletrônicos", 
        "🏠 Imóveis", 
        "🛋️ Casa e Lazer", 
        "👕 Moda", 
        "🛠️ Ferramentas", 
        "✨ Outros"
    ]

def filtrar_por_categoria(query, categoria_selecionada):
    """Aplica o filtro de categoria na consulta do Firebase."""
    if categoria_selecionada and categoria_selecionada != "Todas":
        return query.where("categoria", "==", categoria_selecionada)
    return query