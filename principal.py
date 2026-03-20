# =================================================================
# VRS SISTEMAS
# JÁ VENDEU? - MÓDULO: principal.py
# FUNÇÕES: VITRINE E DETALHES (CARROSSEL ESTILO OLX)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import importlib
import base64

st.set_page_config(page_title="JÁ VENDEU? - Marketplace VRS", layout="wide", initial_sidebar_state="expanded")

import conexao
import interface_javendeu_vrs
import usuarios_vrs
import anuncios_vrs
import categorias
import chat 

importlib.reload(usuarios_vrs)
importlib.reload(chat)

interface_javendeu_vrs.aplicar_estilo_vrs()
db = conexao.conectar_banco_vrs()

if 'pagina_vrs' not in st.session_state: st.session_state['pagina_vrs'] = "Home"
if 'anuncio_detalhe' not in st.session_state: st.session_state['anuncio_detalhe'] = None
if 'foto_index' not in st.session_state: st.session_state['foto_index'] = 0

col_vazia, col_login = st.columns([8, 2])
with col_login:
    if db is not None:
        usuarios_vrs.gerenciar_acesso(db)

interface_javendeu_vrs.obter_menu_lateral_vrs()

if st.session_state['anuncio_detalhe']:
    item = st.session_state['anuncio_detalhe']
    st.markdown(f"## {item.get('titulo', 'Produto')}")
    
    col_img, col_info = st.columns([1.2, 1])
    
    with col_img:
        fotos = item.get('fotos', [])
        if not fotos and 'foto' in item: fotos = [item['foto']]
        
        if fotos:
            idx = st.session_state['foto_index']
            if idx >= len(fotos): idx = 0
            
            # Foto principal travada pelo CSS do interface_vrs
            st.image(f"data:image/jpeg;base64,{fotos[idx]}", use_container_width=True)
            
            # Miniaturas compactas estilo OLX
            if len(fotos) > 1:
                st.markdown('<div class="vrs-galeria">', unsafe_allow_html=True)
                m_cols = st.columns(len(fotos))
                for i in range(len(fotos)):
                    with m_cols[i]:
                        if st.button(f"Foto {i+1}", key=f"thumb_{i}", use_container_width=True):
                            st.session_state['foto_index'] = i
                            st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Sem fotos.")

    with col_info:
        with st.container(border=True):
            st.markdown(f"<h1 style='color: #FF4B4B; margin:0;'>R$ {item.get('preco', 0.0):.2f}</h1>", unsafe_allow_html=True)
            st.info(f"📁 Categoria: {item.get('categoria', 'Geral')}")
            st.write(f"📝 {item.get('descricao', 'Sem descrição.')}")
            st.markdown("---")
            
            if st.button("💬 TENHO INTERESSE / ABRIR CHAT", use_container_width=True, type="primary"):
                if st.session_state.get('logado'):
                    st.session_state['vrs_chat_ativo'] = item['vendedor_email']
                    st.session_state['vrs_produto_atual'] = item['titulo']
                    chat.enviar_mensagem_vrs(db, item['vendedor_email'], f"Olá! Vi seu anúncio '{item['titulo']}' e tenho interesse.", item['titulo'])
                    st.session_state['pagina_vrs'] = "Chat"
                    st.session_state['anuncio_detalhe'] = None
                    st.rerun()
                else:
                    st.error("⚠️ Faça login para conversar.")

            if st.button("⬅️ VOLTAR PARA A VITRINE", use_container_width=True):
                st.session_state['anuncio_detalhe'] = None
                st.session_state['foto_index'] = 0
                st.rerun()

else:
    # Lógica da Home (Vitrine) - Sem alterações para não quebrar nada
    pag = st.session_state['pagina_vrs']
    if pag == "Home":
        interface_javendeu_vrs.exibir_identidade_visual_vrs()
        interface_javendeu_vrs.exibir_conversor_vrs()
        st.markdown("---")
        st.subheader("🛍️ Vitrine de Ofertas")
        cat_filtro = st.selectbox("O que você procura?", ["Todas"] + categorias.obter_categorias_vrs())
        try:
            if db:
                query = db.collection("anuncios").where("status", "==", "ativo")
                if cat_filtro != "Todas": query = query.where("categoria", "==", cat_filtro)
                docs = query.stream()
                lista_anuncios = [d.to_dict() | {"id": d.id} for d in docs if 'titulo' in d.to_dict()]
                if not lista_anuncios:
                    st.warning("🧐 Nenhuma oferta encontrada.")
                else:
                    cols_vitrine = st.columns(4)
                    for idx, anuncio in enumerate(lista_anuncios):
                        with cols_vitrine[idx % 4]:
                            with st.container(border=True):
                                f_capa = anuncio['fotos'][0] if 'fotos' in anuncio and anuncio['fotos'] else anuncio.get('foto', "")
                                if f_capa: st.image(f"data:image/jpeg;base64,{f_capa}", use_container_width=True)
                                st.markdown(f"**{anuncio.get('titulo', 'Sem Título')}**")
                                st.markdown(f"<h4 style='color: #FF4B4B;'>R$ {anuncio.get('preco', 0.0):.2f}</h4>", unsafe_allow_html=True)
                                if st.button("Ver Detalhes", key=f"vit_{anuncio['id']}", use_container_width=True):
                                    st.session_state['anuncio_detalhe'] = anuncio
                                    st.session_state['foto_index'] = 0
                                    st.rerun()
        except Exception as e:
            st.error(f"Erro na vitrine: {e}")
    elif pag in ["Anunciar", "Meus Anúncios"]:
        anuncios_vrs.exibir_painel_vendedor(db)
    elif pag == "Chat":
        chat.exibir_interface_chat(db)

interface_javendeu_vrs.exibir_rodape_vrs()