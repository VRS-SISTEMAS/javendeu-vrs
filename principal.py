# =================================================================
# VRS SISTEMAS
# JÁ VENDEU? - MÓDULO: principal.py (VERSÃO ESTÁVEL ANTI-F5)
# FUNÇÕES: VITRINE, DETALHES E RECUPERAÇÃO DE SESSÃO
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import importlib
import base64
import datetime

st.set_page_config(page_title="JÁ VENDEU? - Marketplace VRS", layout="wide", initial_sidebar_state="expanded")

import conexao
import interface_javendeu_vrs
import usuarios_vrs
import anuncios_vrs
import categorias
import chat 

# Garante atualizações dos módulos em tempo real
importlib.reload(usuarios_vrs)
importlib.reload(anuncios_vrs)

interface_javendeu_vrs.aplicar_estilo_vrs()
db = conexao.conectar_banco_vrs()

# CSS MESTRE VRS (DESIGN E STATUS ONLINE)
st.markdown("""
    <style>
    .moldura-foto-vrs {
        background-color: #0E1117; border: 1px solid #333; border-radius: 10px;
        height: 400px; display: flex; align-items: center; justify-content: center; overflow: hidden;
    }
    .moldura-foto-vrs img { max-height: 400px; max-width: 100%; object-fit: contain; }
    .caixa-comentario { background-color: #1A1C24; padding: 15px; border-radius: 8px; border-left: 4px solid #FF4B4B; margin-bottom: 10px; }
    .ponto-online { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px; box-shadow: 0 0 8px #00FF00; }
    .status-online-vrs { color: #00FF00; font-weight: bold; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

# Inicializa estados de navegação se não existirem
if 'pagina_vrs' not in st.session_state: st.session_state['pagina_vrs'] = "Home"
if 'anuncio_detalhe' not in st.session_state: st.session_state['anuncio_detalhe'] = None

# Cabeçalho com sistema de Login (Gerencia a persistência internamente)
col_vazia, col_login = st.columns([8, 2])
with col_login:
    if db is not None:
        usuarios_vrs.gerenciar_acesso(db)

interface_javendeu_vrs.obter_menu_lateral_vrs()

# --- LÓGICA DE EXIBIÇÃO ---
if st.session_state['anuncio_detalhe']:
    item = st.session_state['anuncio_detalhe']
    anuncios_vrs.exibir_alerta_seguranca_vrs()
    st.markdown(f"## {item.get('titulo')}")
    
    col_img, col_info = st.columns([1.5, 1])
    with col_img:
        fotos = item.get('fotos', [])
        if fotos:
            tabs = st.tabs([f"FOTO {i+1}" for i in range(len(fotos))])
            for i, f_b64 in enumerate(fotos):
                with tabs[i]: st.markdown(f'<div class="moldura-foto-vrs"><img src="data:image/jpeg;base64,{f_b64}"></div>', unsafe_allow_html=True)

    with col_info:
        with st.container(border=True):
            st.markdown(f"<h1 style='color: #FF4B4B; margin:0;'>R$ {item.get('preco', 0.0):.2f}</h1>", unsafe_allow_html=True)
            v_nome = item.get('vendedor_nome', 'Usuário').split()[0].title()
            st.markdown(f"👤 **Vendedor:** {v_nome}")
            st.markdown('<div class="status-online-vrs"><span class="ponto-online"></span>VENDEDOR ONLINE</div>', unsafe_allow_html=True)
            st.markdown(f"📍 **{item.get('cidade')} - {item.get('estado')}**")
            st.markdown("---")
            st.write(item.get('descricao'))
            
            if st.button("💬 CHAT INTERNO", use_container_width=True, type="primary"):
                if st.session_state.get('logado'):
                    st.session_state['vrs_chat_ativo'] = item['vendedor_email']
                    st.session_state['pagina_vrs'] = "Chat"
                    st.rerun()
                else: st.error("Faça login.")
            
            zap = item.get('vendedor_whatsapp')
            if zap: st.link_button("🟢 WHATSAPP", f"https://wa.me/55{zap}", use_container_width=True)
            
            if st.button("⬅️ VOLTAR"):
                st.session_state['anuncio_detalhe'] = None
                st.rerun()
else:
    if st.session_state['pagina_vrs'] == "Home":
        interface_javendeu_vrs.exibir_identidade_visual_vrs()
        st.markdown("---")
        try:
            docs = db.collection("anuncios").where("status", "==", "ativo").stream()
            lista = [d.to_dict() | {"id": d.id} for d in docs]
            if lista:
                cols = st.columns(4)
                for idx, anuncio in enumerate(lista):
                    with cols[idx % 4]:
                        with st.container(border=True):
                            if anuncio.get('fotos'): st.image(f"data:image/jpeg;base64,{anuncio['fotos'][0]}", use_container_width=True)
                            st.write(f"**{anuncio['titulo']}**")
                            if st.button("Ver Detalhes", key=f"v_{anuncio['id']}", use_container_width=True):
                                st.session_state['anuncio_detalhe'] = anuncio
                                st.rerun()
        except: pass
    elif st.session_state['pagina_vrs'] in ["Anunciar", "Meus Anúncios"]:
        anuncios_vrs.exibir_painel_vendedor(db)
    elif st.session_state['pagina_vrs'] == "Chat":
        chat.exibir_interface_chat(db)
    interface_javendeu_vrs.exibir_rodape_vrs()