# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: principal.py (CORAÇÃO DO MARKETPLACE NACIONAL - COMPLETO)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import importlib
import base64
import datetime

# Configuração inicial obrigatória
st.set_page_config(page_title="JÁ VENDEU? - Marketplace VRS", layout="wide", initial_sidebar_state="expanded")

import conexao
import interface_javendeu_vrs
import usuarios_vrs
import anuncios_vrs
import categorias
import chat 
import admin_vrs 
import publicidade_clientes 

# Recarga de módulos para desenvolvimento em tempo real
importlib.reload(usuarios_vrs)
importlib.reload(anuncios_vrs)
importlib.reload(admin_vrs)
importlib.reload(publicidade_clientes)

interface_javendeu_vrs.aplicar_estilo_vrs()
db = conexao.conectar_banco_vrs()

# CSS MESTRE - IDENTIDADE VRS
st.markdown("""
    <style>
    .moldura-foto-vrs { background-color: #0E1117; border: 1px solid #333; border-radius: 10px; height: 400px; display: flex; align-items: center; justify-content: center; overflow: hidden; }
    .moldura-foto-vrs img { max-height: 400px; max-width: 100%; object-fit: contain; }
    .ponto-online { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px; box-shadow: 0 0 8px #00FF00; }
    .status-online-vrs { color: #00FF00; font-weight: bold; font-size: 14px; }
    
    /* Correção visual para os banners de publicidade */
    .vrs-banner-container-fix img {
        transition: 0.3s;
    }
    .vrs-banner-container-fix img:hover {
        transform: scale(1.01);
        border-color: #FF4B4B !important;
    }

    div.stButton > button:first-child[aria-label="💬 NEGOCIAR NO CHAT"] {
        background-color: #FF4B4B !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        height: 50px !important;
    }
    </style>
""", unsafe_allow_html=True)

if 'pagina_vrs' not in st.session_state: st.session_state['pagina_vrs'] = "Home"
if 'anuncio_detalhe' not in st.session_state: st.session_state['anuncio_detalhe'] = None

# Cabeçalho de Acesso
col_vazia, col_login = st.columns([8, 2])
with col_login:
    if db is not None: usuarios_vrs.gerenciar_acesso(db)

interface_javendeu_vrs.obter_menu_lateral_vrs()

# Trava de Menu Administrativo
if st.session_state.get('logado') and st.session_state['usuario']['email'] == "vrsolucoes.sistemas@gmail.com":
    with st.sidebar:
        st.markdown("---")
        if st.button("PAINEL ADMINISTRATIVO", key="btn_admin_vrs", use_container_width=True):
            st.session_state['pagina_vrs'] = "Admin"
            st.session_state['anuncio_detalhe'] = None
            st.rerun()

# --- LÓGICA DE TELAS ---
if st.session_state['anuncio_detalhe']:
    # TELA DE DETALHES DO PRODUTO
    item = st.session_state['anuncio_detalhe']
    st.markdown(f"## {item.get('titulo').upper()}")
    col_img, col_info = st.columns([1.5, 1])
    
    with col_img:
        fotos = item.get('fotos', [])
        if fotos:
            tabs = st.tabs([f"FOTO {i+1}" for i in range(len(fotos))])
            for i, f_b64 in enumerate(fotos):
                with tabs[i]: st.markdown(f'<div class="moldura-foto-vrs"><img src="data:image/jpeg;base64,{f_b64}"></div>', unsafe_allow_html=True)
        else:
            st.info("📷 Sem fotos para este anúncio.")
            
    with col_info:
        with st.container(border=True):
            st.markdown(f"<h1>R$ {item.get('preco', 0.0):.2f}</h1>", unsafe_allow_html=True)
            st.markdown(f"📍 **{item.get('cidade')} - {item.get('estado')}**")
            st.write(item.get('descricao'))
            
            if st.button("💬 NEGOCIAR NO CHAT", use_container_width=True):
                if not st.session_state.get('logado'):
                    st.warning("⚠️ Faça login para negociar.")
                else:
                    st.session_state['pagina_vrs'] = "Chat"
                    st.rerun()

            if st.button("⬅️ VOLTAR PARA VITRINE", use_container_width=True):
                st.session_state['anuncio_detalhe'] = None
                st.rerun()
else:
    # NAVEGAÇÃO ENTRE MÓDULOS
    if st.session_state['pagina_vrs'] == "Home":
        interface_javendeu_vrs.exibir_identidade_visual_vrs()
        st.markdown("---")
        
        # Filtros de Busca
        st.subheader("🛍️ Vitrine de Ofertas")
        f1, f2, f3 = st.columns([2, 1, 2])
        cat_f = f1.selectbox("O que você procura?", ["Todas"] + categorias.obter_categorias_vrs())
        est_f = f2.selectbox("Estado", ["Brasil"] + anuncios_vrs.ESTADOS_BR)
        cid_f = f3.text_input("Cidade (opcional)").strip().title()

        # --- BANNER PUBLICITÁRIO INTELIGENTE ---
        if db:
            publicidade_clientes.exibir_banner_rotativo_vrs(db, estado_atual=est_f)

        # --- EXIBIÇÃO DA VITRINE ---
        try:
            if db:
                docs = db.collection("anuncios").where("status", "==", "ativo").stream()
                lista_anuncios = []
                for d in docs:
                    it = d.to_dict()
                    if (cat_f == "Todas" or it.get('categoria') == cat_f) and \
                       (est_f == "Brasil" or it.get('estado') == est_f) and \
                       (not cid_f or cid_f in it.get('cidade', '')):
                        lista_anuncios.append(it | {"id": d.id})
                
                if not lista_anuncios:
                    st.warning("🧐 Nenhum anúncio encontrado para esta região.")
                else:
                    cols = st.columns(4)
                    for idx, anuncio in enumerate(lista_anuncios):
                        with cols[idx % 4]:
                            with st.container(border=True):
                                f_capa = anuncio['fotos'][0] if anuncio.get('fotos') else ""
                                if f_capa: st.image(f"data:image/jpeg;base64,{f_capa}", use_container_width=True)
                                st.markdown(f"**{anuncio.get('titulo')}**")
                                st.markdown(f"<h4 style='color: #FF4B4B;'>R$ {anuncio.get('preco', 0.0):.2f}</h4>", unsafe_allow_html=True)
                                st.caption(f"📍 {anuncio.get('cidade')} - {anuncio.get('estado')}")
                                if st.button("Ver Detalhes", key=f"vit_{anuncio['id']}", use_container_width=True):
                                    st.session_state['anuncio_detalhe'] = anuncio
                                    st.rerun()
        except Exception as e: 
            st.error("Erro ao carregar os anúncios.")
            
    elif st.session_state['pagina_vrs'] == "Admin":
        admin_vrs.exibir_painel_admin_vrs(db)
    
    elif st.session_state['pagina_vrs'] == "Chat":
        chat.exibir_interface_chat(db)

    interface_javendeu_vrs.exibir_rodape_vrs()