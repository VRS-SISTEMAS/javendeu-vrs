# =================================================================
# VRS SISTEMAS - JÁ VENDEU?
# MÓDULO: interface_javendeu_vrs.py (REGRAS DE SEGURANÇA RESTAURADAS)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st

def aplicar_estilo_vrs():
    """Aplica o CSS da VRS SOLUÇÕES."""
    st.markdown("""
        <style>
        .titulo-vrs-centro { color: #FF4B4B; font-size: 85px; font-weight: 900; text-align: center; text-shadow: 4px 4px 10px #000000; margin-bottom: 0px; font-family: 'Arial Black', sans-serif; }
        .banner-vrs { background-color: #FF4B4B; padding: 30px; border-radius: 4px; text-align: center; color: white; font-weight: 900; margin-top: 10px; }
        [data-testid="stSidebarCollapsedControl"] { display: flex !important; visibility: visible !important; background-color: #FF4B4B !important; border-radius: 0 10px 10px 0 !important; width: 60px !important; height: 60px !important; left: 0 !important; top: 20px !important; z-index: 999999; }
        [data-testid="stSidebarCollapsedControl"] svg { fill: white !important; width: 40px !important; height: 40px !important; }
        header[data-testid="stHeader"] { background: rgba(0,0,0,0); }
        .stImage > img { max-height: 480px !important; width: auto !important; margin-left: auto; margin-right: auto; display: block; border-radius: 12px; object-fit: contain; background-color: #0E1117; border: 1px solid #333; }
        
        /* Ajuste do Banner Publicitário */
        .vrs-banner-fix img { max-height: none !important; width: 100% !important; height: auto !important; border-radius: 10px !important; border: 1px solid #444 !important; }
        
        /* Estilo para os cards de regras no rodapé */
        .vrs-regra-card {
            background-color: #1A1C24;
            padding: 12px;
            border-radius: 8px;
            border-left: 4px solid #FF4B4B;
            margin-bottom: 8px;
        }
        </style>
        """, unsafe_allow_html=True)

def exibir_identidade_visual_vrs():
    """Exibe o logotipo e o slogan principal da plataforma."""
    st.markdown("<h1 class='titulo-vrs-centro'>JÁ VENDEU?</h1>", unsafe_allow_html=True)
    st.markdown("<div class='banner-vrs'><h1 style='margin:0; color:white;'>ANUNCIE GRÁTIS E VENDA RÁPIDO</h1></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; color: #CCCCCC; font-size: 22px; margin-top: 15px; margin-bottom: 40px;'>\"Onde o seu 'parado' vira oportunidade e o seu desejo vira realidade.\"</div>", unsafe_allow_html=True)

def exibir_rodape_vrs():
    """Exibe o rodapé com Regras de Segurança e Termos de Uso (FIXO)."""
    st.markdown("---")
    
    # Bloco de Regras de Segurança que eu tinha removido acidentalmente
    with st.expander("🛡️ REGRAS DE SEGURANÇA E TERMOS DE USO - VRS SISTEMAS", expanded=False):
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown("<h4 style='color: #FF4B4B;'>Dicas para Compradores</h4>", unsafe_allow_html=True)
            st.markdown("""
                <div class='vrs-regra-card'>🤝 <b>Encontros:</b> Sempre marque em locais públicos e movimentados.</div>
                <div class='vrs-regra-card'>💰 <b>Pagamentos:</b> Nunca faça depósitos ou transferências antecipadas.</div>
            """, unsafe_allow_html=True)
        with col_r2:
            st.markdown("<h4 style='color: #FF4B4B;'>Dicas para Vendedores</h4>", unsafe_allow_html=True)
            st.markdown("""
                <div class='vrs-regra-card'>📸 <b>Anúncios:</b> Use fotos reais e seja honesto na descrição.</div>
                <div class='vrs-regra-card'>💳 <b>Recebimento:</b> Só entregue o produto após confirmar o dinheiro na conta.</div>
            """, unsafe_allow_html=True)
        
        st.markdown("<p style='font-size: 12px; text-align: center; color: #888;'>A VRS SISTEMAS não cobra taxas e não se responsabiliza pelas negociações entre usuários.</p>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: center; color: #444; font-size: 11px; margin-top: 15px;'>© 2026 JÁ VENDEU? | Orgulhosamente desenvolvido por VRS SISTEMAS</p>", unsafe_allow_html=True)

def obter_menu_lateral_vrs():
    """Gerencia a navegação lateral da plataforma."""
    if 'pagina_vrs' not in st.session_state: st.session_state['pagina_vrs'] = "Home"
    with st.sidebar:
        st.markdown("<h2 style='color: #FF4B4B;'>MENU VRS</h2>", unsafe_allow_html=True)
        
        if st.button("🏠 HOME", key="menu_home", use_container_width=True):
            st.session_state['pagina_vrs'] = "Home"
            st.session_state['anuncio_detalhe'] = None
            st.rerun()
            
        if st.session_state.get('logado'):
            if st.button("➕ ANUNCIAR", key="menu_anunciar", use_container_width=True): 
                st.session_state['pagina_vrs'] = "Anunciar"
                st.rerun()
            if st.button("🗂️ MEUS ANÚNCIOS", key="menu_meus", use_container_width=True): 
                st.session_state['pagina_vrs'] = "Meus Anúncios"
                st.rerun()
            if st.button("💬 CHAT", key="menu_chat", use_container_width=True): 
                st.session_state['pagina_vrs'] = "Chat"
                st.rerun()
                
    return st.session_state['pagina_vrs']