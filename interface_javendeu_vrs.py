# =================================================================
# VRS SISTEMAS
# JÁ VENDEU? - INTERFACE MESTRE COM DESIGN OLX STYLE
# MÓDULO: interface_javendeu_vrs.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st

def aplicar_estilo_vrs():
    """Aplica o CSS customizado para manter a identidade visual da VRS SISTEMAS."""
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
        
        [data-testid="stSidebarCollapsedControl"] svg {
            fill: white !important;
            width: 40px !important;
            height: 40px !important;
        }

        header[data-testid="stHeader"] { background: rgba(0,0,0,0); }

        /* --- DESIGN OLX: CONTROLE DE IMAGEM --- */
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

        /* Galeria de miniaturas */
        .vrs-galeria {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 10px;
        }

        /* Estilo para as Regras de Segurança */
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
    """Rodapé com Termos de Uso e Regras de Segurança detalhadas."""
    st.markdown("---")
    with st.expander("🛡️ REGRAS DE SEGURANÇA E TERMOS DE USO - VRS SISTEMAS"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h4 style='color: #FF4B4B;'>Dicas para Compradores</h4>", unsafe_allow_html=True)
            st.markdown("""
            <div class='vrs-regra-card'>🤝 <b>Encontros:</b> Sempre prefira locais públicos e movimentados para ver o produto.</div>
            <div class='vrs-regra-card'>💰 <b>Pagamentos:</b> Nunca antecipe pagamentos sem ter visto o produto pessoalmente.</div>
            <div class='vrs-regra-card'>🔍 <b>Verificação:</b> Teste o funcionamento de eletrônicos antes de fechar o negócio.</div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("<h4 style='color: #FF4B4B;'>Dicas para Vendedores</h4>", unsafe_allow_html=True)
            st.markdown("""
            <div class='vrs-regra-card'>📸 <b>Transparência:</b> Use fotos reais e descreva honestamente o estado do produto.</div>
            <div class='vrs-regra-card'>💳 <b>Confirmação:</b> Só entregue o produto após confirmar o dinheiro na conta (cuidado com comprovantes falsos).</div>
            <div class='vrs-regra-card'>🚫 <b>Dados Pessoais:</b> Evite compartilhar dados sensíveis fora do chat da plataforma.</div>
            """, unsafe_allow_html=True)

        st.markdown("<br><h4 style='color: #FF4B4B; text-align: center;'>Termos de Uso</h4>", unsafe_allow_html=True)
        st.caption("""
        O 'JÁ VENDEU?' é uma plataforma de classificados online desenvolvida pela VRS SISTEMAS. 
        Não intermediamos pagamentos nem entregas. A responsabilidade da negociação é exclusiva entre comprador e vendedor. 
        É proibido o anúncio de itens ilícitos, armas ou serviços que violem as leis vigentes.
        """)

    st.markdown("""
        <div style='margin-top: 30px; padding: 40px; text-align: center; border-top: 1px solid #333; background-color: #111;'>
            <p style='color: #444; font-size: 11px;'>© 2026 JÁ VENDEU? | Orgulhosamente desenvolvido por VRS SISTEMAS</p>
        </div>
    """, unsafe_allow_html=True)

def obter_menu_lateral_vrs():
    """Gerencia a navegação através da barra lateral."""
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