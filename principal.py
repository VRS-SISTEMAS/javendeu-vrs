# =================================================================
# VRS SISTEMAS
# JÁ VENDEU? - MÓDULO: principal.py
# FUNÇÕES: VITRINE E DETALHES (FILTROS DE LOCALIZAÇÃO INTEGRADOS)
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

# CSS MESTRE PARA TRAVAR O TAMANHO DAS FOTOS
st.markdown("""
    <style>
    .moldura-foto-vrs {
        background-color: #0E1117;
        border: 1px solid #333;
        border-radius: 10px;
        height: 400px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }
    .moldura-foto-vrs img {
        max-height: 400px;
        max-width: 100%;
        object-fit: contain;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        padding: 0 20px;
        background-color: #1A1C24;
        border-radius: 5px 5px 0 0;
    }
    </style>
""", unsafe_allow_html=True)

if 'pagina_vrs' not in st.session_state: st.session_state['pagina_vrs'] = "Home"
if 'anuncio_detalhe' not in st.session_state: st.session_state['anuncio_detalhe'] = None

col_vazia, col_login = st.columns([8, 2])
with col_login:
    if db is not None:
        usuarios_vrs.gerenciar_acesso(db)

interface_javendeu_vrs.obter_menu_lateral_vrs()

# --- LÓGICA DE EXIBIÇÃO ---
if st.session_state['anuncio_detalhe']:
    item = st.session_state['anuncio_detalhe']
    st.markdown(f"## {item.get('titulo', 'Produto')}")
    
    col_img, col_info = st.columns([1.5, 1])
    
    with col_img:
        fotos = item.get('fotos', [])
        if not fotos and 'foto' in item: fotos = [item['foto']]
        if fotos:
            titulos_fotos = [f"FOTO {i+1}" for i in range(len(fotos))]
            tabs_carrossel = st.tabs(titulos_fotos)
            for i, f_b64 in enumerate(fotos):
                with tabs_carrossel[i]:
                    st.markdown(f'<div class="moldura-foto-vrs"><img src="data:image/jpeg;base64,{f_b64}"></div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Sem fotos disponíveis.")

    with col_info:
        with st.container(border=True):
            st.markdown(f"<h1 style='color: #FF4B4B; margin:0;'>R$ {item.get('preco', 0.0):.2f}</h1>", unsafe_allow_html=True)
            st.markdown(f"📍 **{item.get('cidade', 'N/A')} - {item.get('estado', 'N/A')}**")
            st.markdown(f"**📁 Categoria:** {item.get('categoria', 'Geral')}")
            st.markdown("---")
            st.write("**Descrição:**")
            st.write(item.get('descricao', 'Sem descrição.'))
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("💬 TENHO INTERESSE / ABRIR CHAT", key="btn_chat_detalhe", use_container_width=True, type="primary"):
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
                st.rerun()

else:
    pag = st.session_state['pagina_vrs']
    if pag == "Home":
        interface_javendeu_vrs.exibir_identidade_visual_vrs()
        interface_javendeu_vrs.exibir_conversor_vrs()
        st.markdown("---")
        
        # --- BARRA DE BUSCA E FILTROS INTELIGENTES ---
        st.subheader("🛍️ Vitrine de Ofertas")
        f_col1, f_col2, f_col3 = st.columns([2, 1, 2])
        
        cat_filtro = f_col1.selectbox("O que você procura?", ["Todas"] + categorias.obter_categorias_vrs())
        est_filtro = f_col2.selectbox("Estado", ["Brasil"] + anuncios_vrs.ESTADOS_BR)
        cid_filtro = f_col3.text_input("Cidade (opcional)", placeholder="Ex: Duque de Caxias").strip().title()

        try:
            if db:
                query = db.collection("anuncios").where("status", "==", "ativo")
                
                # Filtros aplicados no código (devido a limitações de índices do Firebase)
                docs = query.stream()
                lista_anuncios = []
                
                for d in docs:
                    item = d.to_dict()
                    # Aplicando lógica de filtro
                    match_cat = (cat_filtro == "Todas" or item.get('categoria') == cat_filtro)
                    match_est = (est_filtro == "Brasil" or item.get('estado') == est_filtro)
                    match_cid = (not cid_filtro or cid_filtro in item.get('cidade', ''))
                    
                    if match_cat and match_est and match_cid:
                        lista_anuncios.append(item | {"id": d.id})

                if not lista_anuncios:
                    st.warning("🧐 Nenhuma oferta encontrada para os filtros selecionados.")
                else:
                    cols_vitrine = st.columns(4)
                    for idx, anuncio in enumerate(lista_anuncios):
                        with cols_vitrine[idx % 4]:
                            with st.container(border=True):
                                f_capa = anuncio['fotos'][0] if 'fotos' in anuncio and anuncio['fotos'] else anuncio.get('foto', "")
                                if f_capa: 
                                    st.image(f"data:image/jpeg;base64,{f_capa}", use_container_width=True)
                                st.markdown(f"**{anuncio.get('titulo', 'Sem Título')}**")
                                st.markdown(f"<h4 style='color: #FF4B4B;'>R$ {anuncio.get('preco', 0.0):.2f}</h4>", unsafe_allow_html=True)
                                st.caption(f"📍 {anuncio.get('cidade', 'N/A')} ({anuncio.get('estado', 'N/A')})")
                                if st.button("Ver Detalhes", key=f"vit_{anuncio['id']}", use_container_width=True):
                                    st.session_state['anuncio_detalhe'] = anuncio
                                    st.rerun()
        except Exception as e:
            st.error(f"Erro na vitrine: {e}")
            
    elif pag in ["Anunciar", "Meus Anúncios"]:
        anuncios_vrs.exibir_painel_vendedor(db)
    elif pag == "Chat":
        chat.exibir_interface_chat(db)

    interface_javendeu_vrs.exibir_rodape_vrs()