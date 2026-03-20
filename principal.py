# =================================================================
# VRS SISTEMAS
# JÁ VENDEU? - MÓDULO: principal.py
# FUNÇÕES: VITRINE E DETALHES (CARROSSEL REAL ESTILO OLX)
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

# CSS Extra para travar o tamanho da imagem e estilizar as miniaturas
st.markdown("""
    <style>
    /* Trava a imagem principal para não ficar gigante */
    .img-principal-vrs img {
        max-height: 450px !important;
        object-fit: contain !important;
        background-color: #000;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    /* Estilo das miniaturas clicáveis */
    .stButton > button.vrs-thumb-btn {
        border: 2px solid #333;
        padding: 0px;
        border-radius: 5px;
        overflow: hidden;
    }
    .stButton > button.vrs-thumb-btn:hover {
        border-color: #FF4B4B;
    }
    </style>
""", unsafe_allow_html=True)

if 'pagina_vrs' not in st.session_state: st.session_state['pagina_vrs'] = "Home"
if 'anuncio_detalhe' not in st.session_state: st.session_state['anuncio_detalhe'] = None
if 'foto_index' not in st.session_state: st.session_state['foto_index'] = 0

col_vazia, col_login = st.columns([8, 2])
with col_login:
    if db is not None:
        usuarios_vrs.gerenciar_acesso(db)

interface_javendeu_vrs.obter_menu_lateral_vrs()

# --- LÓGICA DE EXIBIÇÃO ---
if st.session_state['anuncio_detalhe']:
    # SEÇÃO: DETALHES DO PRODUTO (Estilo Carrossel OLX)
    item = st.session_state['anuncio_detalhe']
    st.markdown(f"## {item.get('titulo', 'Produto')}")
    
    col_img, col_info = st.columns([1.3, 1])
    
    with col_img:
        fotos = item.get('fotos', [])
        if not fotos and 'foto' in item: fotos = [item['foto']]
        
        if fotos:
            idx = st.session_state['foto_index']
            if idx >= len(fotos): idx = 0
            
            # EXIBIÇÃO DA FOTO PRINCIPAL (COM TRAVA DE TAMANHO)
            st.markdown('<div class="img-principal-vrs">', unsafe_allow_html=True)
            st.image(f"data:image/jpeg;base64,{fotos[idx]}", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # MINIATURAS ESTILO CARROSSEL (FOTOS REAIS EMBAIXO)
            if len(fotos) > 1:
                st.markdown("---")
                # Criamos colunas pequenas para as miniaturas
                m_cols = st.columns(8) # Até 8 espaços para ficar alinhado
                for i in range(len(fotos)):
                    with m_cols[i]:
                        # Botão que mostra a própria foto como miniatura
                        if st.button(f"📷", key=f"thumb_vrs_{i}", use_container_width=True, help="Ver foto"):
                            st.session_state['foto_index'] = i
                            st.rerun()
                        # Mostra a fotinho pequena embaixo do botão para o usuário saber qual é
                        st.image(f"data:image/jpeg;base64,{fotos[i]}", width=60)
        else:
            st.warning("⚠️ Sem fotos disponíveis.")

    with col_info:
        with st.container(border=True):
            st.markdown(f"<h1 style='color: #FF4B4B; margin:0;'>R$ {item.get('preco', 0.0):.2f}</h1>", unsafe_allow_html=True)
            st.info(f"📁 Categoria: {item.get('categoria', 'Geral')}")
            st.write(f"**Descrição:**")
            st.write(item.get('descricao', 'Sem descrição.'))
            st.markdown("---")
            
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
                st.session_state['foto_index'] = 0
                st.rerun()

else:
    # SEÇÃO: PÁGINAS GERAIS (Vitrine, Anunciar, Meus Anúncios)
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
                                # Foto de capa da vitrine
                                f_capa = anuncio['fotos'][0] if 'fotos' in anuncio and anuncio['fotos'] else anuncio.get('foto', "")
                                if f_capa: 
                                    st.image(f"data:image/jpeg;base64,{f_capa}", use_container_width=True)
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

    # CHAMADA DO RODAPÉ
    interface_javendeu_vrs.exibir_rodape_vrs()