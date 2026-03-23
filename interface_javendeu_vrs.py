# =================================================================
# VRS SISTEMAS - JÁ VENDEU?
# MÓDULO: interface_javendeu_vrs.py (VERSÃO OTIMIZADA PARA BANNERS)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st

def aplicar_estilo_vrs():
    """Aplica o CSS customizado para manter a identidade visual da VRS SISTEMAS."""
    st.markdown("""
        <style>
        .titulo-vrs-centro {
            color: #FF4B4B;
            font-size: 85px;
            font-weight: 900;
            text-align: center;
            text-shadow: 4px 4px 10px #000000;
            margin-bottom: 0px;
            font-family: 'Arial Black', sans-serif;
        }
        .banner-vrs {
            background-color: #FF4B4B;
            padding: 30px;
            border-radius: 4px;
            text-align: center;
            color: white;
            font-weight: 900;
            margin-top: 10px;
        }

        [data-testid="stSidebarCollapsedControl"] {
            display: flex !important;
            visibility: visible !important;
            background-color: #FF4B4B !important;
            border-radius: 0 10px 10px 0 !important;
            width: 60px !important;
            height: 60px !important;
            left: 0 !important;
            top: 20px !important;
            z-index: 999999;
        }

        header[data-testid="stHeader"] { background: rgba(0,0,0,0); }

        /* Estilo para imagens de produtos da vitrine */
        .stImage > img {
            max-height: 480px !important;
            width: auto !important;
            margin-left: auto;
            margin-right: auto;
            display: block;
            border-radius: 12px;
            object-fit: contain;
            background-color: #0E1117;
            border: 1px solid #333;
        }

        /* --- CORREÇÃO PARA BANNERS PUBLICITÁRIOS (VRS) --- */
        .vrs-banner-fix img {
            max-height: none !important;
            width: 100% !important;
            height: auto !important;
            border-radius: 10px !important;
            margin-bottom: 20px !important;
            border: 1px solid #444 !important;
            display: block !important;
        }
        .vrs-banner-fix a:hover img {
            border-color: #FF4B4B !important;
            box-shadow: 0px 0px 15px rgba(255, 75, 75, 0.3);
        }

        .vrs-regra-card {
            background-color: #1A1C24;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #FF4B4B;
            margin-bottom: 10px;
            text-align: left;
        }
        </style>
        """, unsafe_allow_html=True)

def exibir_identidade_visual_vrs():
    st.markdown("<h1 class='titulo-vrs-centro'>JÁ VENDEU?</h1>", unsafe_allow_html=True)
    st.markdown("<div class='banner-vrs'><h1 style='margin:0; color:white;'>ANUNCIE GRÁTIS E VENDA RÁPIDO</h1></div>", unsafe_allow_html=True)

def exibir_rodape_vrs():
    st.markdown("---")
    with st.expander("🛡️ REGRAS DE SEGURANÇA E TERMOS DE USO - VRS SISTEMAS"):
        st.write("A responsabilidade da negociação é exclusiva entre comprador e vendedor.")

def obter_menu_lateral_vrs():
    if 'pagina_vrs' not in st.session_state: st.session_state['pagina_vrs'] = "Home"
    with st.sidebar:
        st.markdown("<h2 style='color: #FF4B4B;'>MENU VRS</h2>", unsafe_allow_html=True)
        if st.button("🏠 HOME", key="menu_home", use_container_width=True):
            st.session_state['pagina_vrs'] = "Home"
            st.rerun()
        if st.session_state.get('logado'):
            if st.button("➕ ANUNCIAR", key="menu_anunciar", use_container_width=True): 
                st.session_state['pagina_vrs'] = "Anunciar"
                st.rerun()
            if st.button("🗂️ MEUS ANÚNCIOS", key="menu_meus", use_container_width=True): 
                st.session_state['pagina_vrs'] = "Meus Anúncios"
                st.rerun()
    return st.session_state['pagina_vrs']