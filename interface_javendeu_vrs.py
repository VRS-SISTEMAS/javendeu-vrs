# =================================================================
# VRS Soluções
# JÁ VENDEU? - INTERFACE MESTRE COM BOTÃO DE RESGATE DA BARRA
# MÓDULO: interface_javendeu_vrs.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st

def aplicar_estilo_vrs():
    """Aplica o CSS customizado para manter a identidade visual da VRS Soluções."""
    st.markdown("""
        <style>
        /* Estilo do Título Central */
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

        /* BOTÃO DE RESGATE DA BARRA LATERAL (Sidebar Control) */
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
        
        /* Cor da setinha branca dentro do controle vermelho */
        [data-testid="stSidebarCollapsedControl"] svg {
            fill: white !important;
            width: 40px !important;
            height: 40px !important;
        }

        /* Deixa o header transparente para focar no design */
        header[data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }
        </style>
        """, unsafe_allow_html=True)

def exibir_identidade_visual_vrs():
    """Mostra a logo e o banner principal da plataforma."""
    st.markdown("<h1 class='titulo-vrs-centro'>JÁ VENDEU?</h1>", unsafe_allow_html=True)
    st.markdown("<div class='banner-vrs'><h1 style='margin:0; color:white;'>ANUNCIE GRÁTIS E VENDA RÁPIDO</h1></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; color: #CCCCCC; font-size: 22px; margin-top: 15px; margin-bottom: 40px;'>\"Onde o seu 'parado' vira oportunidade e o seu desejo vira realidade.\"</div>", unsafe_allow_html=True)

def exibir_conversor_vrs():
    """Link útil para o usuário redimensionar fotos."""
    st.markdown("""
        <div style='background-color: #1A1C24; padding: 20px; border-left: 5px solid #FF4B4B; border-radius: 4px; margin-bottom: 25px;'>
            <strong style='color: #FF4B4B;'>📸 CONVERSOR DE FOTOS VRS:</strong><br>
            <span style='color: #E0E0E0;'>Converta suas fotos para não dar problema no anúncio!</span><br><br>
            <a href='https://www.iloveimg.com/pt/redimensionar-imagem' target='_blank' 
               style='background-color: #FF4B4B; color: white; padding: 8px 15px; text-decoration: none; font-weight: bold; border-radius: 4px;'>
               🔗 ACESSAR CONVERSOR
            </a>
        </div>
    """, unsafe_allow_html=True)

def exibir_rodape_vrs():
    """Rodapé com assinatura da marca."""
    st.markdown("""
        <div style='margin-top: 80px; padding: 40px; text-align: center; border-top: 1px solid #333; background-color: #111;'>
            <h4 style='color: #FF4B4B;'>📜 REGRAS E SEGURANÇA</h4>
            <p style='color: #444; font-size: 11px; margin-top: 25px;'>© 2026 JÁ VENDEU? | Desenvolvido por VRS Soluções</p>
        </div>
    """, unsafe_allow_html=True)

def obter_menu_lateral_vrs():
    """Gerencia a navegação através da barra lateral."""
    with st.sidebar:
        st.markdown("<h2 style='color: #FF4B4B;'>MENU VRS</h2>", unsafe_allow_html=True)
        if st.button("🏠 HOME", use_container_width=True):
            st.session_state['pagina_vrs'] = "Home"
            st.session_state['anuncio_detalhe'] = None
            st.rerun()
        
        # Só exibe opções extras se o usuário estiver logado
        if st.session_state.get('logado'):
            if st.button("➕ ANUNCIAR", use_container_width=True): 
                st.session_state['pagina_vrs'] = "Anunciar"
                st.rerun()
            if st.button("🗂️ MEUS ANÚNCIOS", use_container_width=True): 
                st.session_state['pagina_vrs'] = "Meus Anúncios"
                st.rerun()
            if st.button("💬 CHAT", use_container_width=True): 
                st.session_state['pagina_vrs'] = "Chat"
                st.rerun()
    return st.session_state['pagina_vrs']