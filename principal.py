# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: principal.py (CORAÇÃO DO MARKETPLACE - VERSÃO BLINDADA)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import importlib
import base64
import datetime

# Configuração inicial obrigatória da página
st.set_page_config(page_title="JÁ VENDEU? - Marketplace VRS", layout="wide", initial_sidebar_state="expanded")

# Importação dos módulos do ecossistema VRS Soluções
import conexao
import interface_javendeu_vrs
import usuarios_vrs
import anuncios_vrs
import categorias
import chat 
import admin_vrs 
import publicidade_clientes 

# Forçar recarregamento total para aplicar alterações em tempo real
importlib.reload(usuarios_vrs)
importlib.reload(anuncios_vrs)
importlib.reload(admin_vrs)
importlib.reload(publicidade_clientes)

# Aplicação da Identidade Visual VRS
interface_javendeu_vrs.aplicar_estilo_vrs()
db = conexao.conectar_banco_vrs()

# CSS MESTRE - IDENTIDADE VISUAL VRS
st.markdown("""
    <style>
    .moldura-foto-vrs { background-color: #0E1117; border: 1px solid #333; border-radius: 10px; height: 400px; display: flex; align-items: center; justify-content: center; overflow: hidden; }
    .moldura-foto-vrs img { max-height: 400px; max-width: 100%; object-fit: contain; }
    .ponto-online { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px; box-shadow: 0 0 8px #00FF00; }
    .status-online-vrs { color: #00FF00; font-weight: bold; font-size: 14px; }
    
    div.stButton > button:first-child[aria-label="💬 NEGOCIAR NO CHAT"] {
        background-color: #FF4B4B !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        height: 50px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialização de variáveis de estado
if 'pagina_vrs' not in st.session_state: st.session_state['pagina_vrs'] = "Home"
if 'anuncio_detalhe' not in st.session_state: st.session_state['anuncio_detalhe'] = None

# Cabeçalho de Login
col_vazia, col_login = st.columns([8, 2])
with col_login:
    if db is not None: usuarios_vrs.gerenciar_acesso(db)

# Menu Lateral (Anunciar, Meus Anúncios, Chat, Home)
interface_javendeu_vrs.obter_menu_lateral_vrs()

# --- TRAVA DE SEGURANÇA MESTRE: MENU ADMIN EXCLUSIVO DO VITOR ---
if st.session_state.get('logado') and st.session_state['usuario']['email'] == "vrsolucoes.sistemas@gmail.com":
    with st.sidebar:
        st.markdown("---")
        st.markdown("<h3 style='color: #FF4B4B;'>🛠️ GESTÃO MASTER</h3>", unsafe_allow_html=True)
        if st.button("PAINEL ADMINISTRATIVO", key="btn_admin_vrs", use_container_width=True):
            st.session_state['pagina_vrs'] = "Admin"
            st.session_state['anuncio_detalhe'] = None
            st.rerun()

# --- SISTEMA DE NAVEGAÇÃO DE PÁGINAS ---
if st.session_state['anuncio_detalhe']:
    # TELA DE DETALHES DO PRODUTO
    item = st.session_state['anuncio_detalhe']
    st.markdown(f"## {item.get('titulo', 'ANÚNCIO').upper()}")
    col_img, col_info = st.columns([1.5, 1])
    
    with col_img:
        fotos = item.get('fotos', [])
        if fotos:
            tabs = st.tabs([f"FOTO {i+1}" for i in range(len(fotos))])
            for i, f_b64 in enumerate(fotos):
                with tabs[i]: st.markdown(f'<div class="moldura-foto-vrs"><img src="data:image/jpeg;base64,{f_b64}"></div>', unsafe_allow_html=True)
    
    with col_info:
        with st.container(border=True):
            preco = item.get('preco', 0.0)
            st.markdown(f"<h1 style='color: #FF4B4B; margin:0;'>R$ {preco:.2f}</h1>", unsafe_allow_html=True)
            # LOCALIZAÇÃO NA TELA DE DETALHES
            st.markdown(f"📍 **{item.get('cidade', 'N/I')} - {item.get('estado', 'N/I')}**")
            st.write(item.get('descricao', 'Sem descrição disponível.'))
            
            if st.button("⬅️ VOLTAR PARA VITRINE", use_container_width=True):
                st.session_state['anuncio_detalhe'] = None
                st.rerun()
else:
    # NAVEGAÇÃO PRINCIPAL
    if st.session_state['pagina_vrs'] == "Home":
        interface_javendeu_vrs.exibir_identidade_visual_vrs()
        st.markdown("---")
        
        # Filtros de busca
        st.subheader("🛍️ Vitrine de Ofertas")
        f1, f2, f3 = st.columns([2, 1, 2])
        cat_f = f1.selectbox("O que você procura?", ["Todas"] + categorias.obter_categorias_vrs())
        est_f = f2.selectbox("Estado", ["Brasil"] + anuncios_vrs.ESTADOS_BR)
        cid_f = f3.text_input("Cidade (opcional)").strip().title()

        # --- BANNER PUBLICITÁRIO INTELIGENTE ---
        if db:
            publicidade_clientes.exibir_banner_rotativo_vrs(db, estado_atual=est_f)

        # --- CARREGAMENTO DA VITRINE BLINDADA ---
        try:
            if db:
                docs = db.collection("anuncios").where("status", "==", "ativo").stream()
                lista_anuncios = []
                for d in docs:
                    it = d.to_dict()
                    # Filtro de busca
                    if (cat_f == "Todas" or it.get('categoria') == cat_f) and \
                       (est_f == "Brasil" or it.get('estado') == est_f) and \
                       (not cid_f or cid_f in it.get('cidade', '')):
                        lista_anuncios.append(it | {"id": d.id})

                if not lista_anuncios:
                    st.warning("🧐 Nenhuma oferta encontrada para esta região.")
                else:
                    cols = st.columns(4) 
                    for idx, anuncio in enumerate(lista_anuncios):
                        with cols[idx % 4]:
                            with st.container(border=True):
                                # Verificação segura de fotos
                                fotos_list = anuncio.get('fotos', [])
                                f_capa = fotos_list[0] if fotos_list else ""
                                if f_capa: 
                                    st.image(f"data:image/jpeg;base64,{f_capa}", use_container_width=True)
                                
                                st.markdown(f"**{anuncio.get('titulo', 'Sem Título')}**")
                                preco_card = anuncio.get('preco', 0.0)
                                st.markdown(f"<h4 style='color: #FF4B4B;'>R$ {preco_card:.2f}</h4>", unsafe_allow_html=True)
                                
                                # LOCALIZAÇÃO NOS CARDS
                                st.caption(f"📍 {anuncio.get('cidade', 'N/I')} - {anuncio.get('estado', 'N/I')}")
                                
                                if st.button("Ver Detalhes", key=f"vit_{anuncio['id']}", use_container_width=True):
                                    st.session_state['anuncio_detalhe'] = anuncio
                                    st.rerun()
        except Exception as e: 
            st.error("Erro ao carregar a vitrine. Verifique a conexão com o banco.")

    # --- PÁGINAS DE GESTÃO E CHAT ---
    elif st.session_state['pagina_vrs'] in ["Anunciar", "Meus Anúncios"]:
        anuncios_vrs.exibir_painel_vendedor(db)
    
    elif st.session_state['pagina_vrs'] == "Chat":
        chat.exibir_interface_chat(db)
        
    elif st.session_state['pagina_vrs'] == "Admin":
        admin_vrs.exibir_painel_admin_vrs(db)

    interface_javendeu_vrs.exibir_rodape_vrs()