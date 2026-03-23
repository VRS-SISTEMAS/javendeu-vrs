# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: principal.py (CORAÇÃO DO MARKETPLACE NACIONAL - CORRIGIDO)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import importlib
import base64
import datetime

# Configuração inicial obrigatória da página
st.set_page_config(page_title="JÁ VENDEU? - Marketplace VRS", layout="wide", initial_sidebar_state="expanded")

# Importação dos módulos do sistema VRS
import conexao
import interface_javendeu_vrs
import usuarios_vrs
import anuncios_vrs
import categorias
import chat 
import admin_vrs 

# Forçar recarregamento para aplicar alterações em tempo real
importlib.reload(usuarios_vrs)
importlib.reload(anuncios_vrs)
importlib.reload(admin_vrs)

# Aplicação da Identidade Visual VRS
interface_javendeu_vrs.aplicar_estilo_vrs()
db = conexao.conectar_banco_vrs()

# CSS MESTRE - ESTILIZAÇÃO CUSTOMIZADA
st.markdown("""
    <style>
    .moldura-foto-vrs { background-color: #0E1117; border: 1px solid #333; border-radius: 10px; height: 400px; display: flex; align-items: center; justify-content: center; overflow: hidden; }
    .moldura-foto-vrs img { max-height: 400px; max-width: 100%; object-fit: contain; }
    .ponto-online { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px; box-shadow: 0 0 8px #00FF00; }
    .status-online-vrs { color: #00FF00; font-weight: bold; font-size: 14px; }
    
    /* Botão de Negociação Destacado - Identidade VRS */
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

# Menu Lateral de Navegação
interface_javendeu_vrs.obter_menu_lateral_vrs()

# --- TRAVA DE SEGURANÇA MESTRE: MENU ADMIN EXCLUSIVO DO VITOR (VRS SOLUÇÕES) ---
if st.session_state.get('logado') and st.session_state['usuario']['email'] == "vrsolucoes.sistemas@gmail.com":
    with st.sidebar:
        st.markdown("---")
        st.markdown("<h3 style='color: #FF4B4B;'>🛠️ GESTÃO VRS</h3>", unsafe_allow_html=True)
        if st.button("PAINEL ADMINISTRATIVO", key="btn_admin_vrs", use_container_width=True):
            st.session_state['pagina_vrs'] = "Admin"
            st.session_state['anuncio_detalhe'] = None
            st.rerun()

# --- TELA DE DETALHES DO PRODUTO ---
if st.session_state['anuncio_detalhe']:
    item = st.session_state['anuncio_detalhe']
    anuncios_vrs.exibir_alerta_seguranca_vrs()
    st.markdown(f"## {item.get('titulo').upper()}")
    col_img, col_info = st.columns([1.5, 1])
    
    with col_img:
        fotos = item.get('fotos', [])
        if fotos:
            tabs = st.tabs([f"FOTO {i+1}" for i in range(len(fotos))])
            for i, f_b64 in enumerate(fotos):
                with tabs[i]: st.markdown(f'<div class="moldura-foto-vrs"><img src="data:image/jpeg;base64,{f_b64}"></div>', unsafe_allow_html=True)
        else:
            st.info("📷 Este anúncio não possui fotos.")

    with col_info:
        with st.container(border=True):
            st.markdown(f"<h1 style='color: #FF4B4B; margin:0;'>R$ {item.get('preco', 0.0):.2f}</h1>", unsafe_allow_html=True)
            v_nome = item.get('vendedor_nome', 'Usuário').split()[0].title()
            st.markdown(f"👤 **Vendedor:** {v_nome} | <span class='status-online-vrs'><span class='ponto-online'></span>ONLINE</span>", unsafe_allow_html=True)
            st.markdown(f"📍 **{item.get('cidade')} - {item.get('estado')}**")
            st.write(item.get('descricao'))
            
            # Botão de Negociação (Encaminha para o Chat em tempo real)
            if st.button("💬 NEGOCIAR NO CHAT", use_container_width=True):
                if not st.session_state.get('logado'):
                    st.warning("⚠️ Você precisa estar logado para negociar!")
                elif item['vendedor_email'] == st.session_state['usuario']['email']:
                    st.error("🚫 Você não pode negociar seu próprio produto!")
                else:
                    st.session_state['vrs_chat_ativo'] = item['vendedor_email']
                    st.session_state['vrs_nome_ativo'] = v_nome
                    st.session_state['vrs_produto_atual'] = item['titulo']
                    st.session_state['pagina_vrs'] = "Chat"
                    st.session_state['anuncio_detalhe'] = None
                    st.rerun()

            if st.button("⬅️ VOLTAR", use_container_width=True):
                st.session_state['anuncio_detalhe'] = None
                st.rerun()

# --- SISTEMA DE NAVEGAÇÃO DE PÁGINAS ---
else:
    if st.session_state['pagina_vrs'] == "Home":
        interface_javendeu_vrs.exibir_identidade_visual_vrs()
        st.markdown("---")
        
        # Filtros de busca com suporte Nacional
        st.subheader("🛍️ Vitrine de Ofertas")
        f1, f2, f3 = st.columns([2, 1, 2])
        cat_f = f1.selectbox("O que você procura?", ["Todas"] + categorias.obter_categorias_vrs())
        est_f = f2.selectbox("Estado", ["Brasil"] + anuncios_vrs.ESTADOS_BR)
        cid_f = f3.text_input("Cidade (opcional)", placeholder="Ex: Duque de Caxias").strip().title()

        try:
            if db:
                # Busca ativa no Firestore
                docs = db.collection("anuncios").where("status", "==", "ativo").stream()
                lista_anuncios = []
                for d in docs:
                    it = d.to_dict()
                    # Lógica de Filtro Nacional (VRS Soluções)
                    if (cat_f == "Todas" or it.get('categoria') == cat_f) and \
                       (est_f == "Brasil" or it.get('estado') == est_f) and \
                       (not cid_f or cid_f in it.get('cidade', '')):
                        lista_anuncios.append(it | {"id": d.id})

                # Ordenação: VIPs aparecem primeiro na vitrine
                lista_anuncios = sorted(lista_anuncios, key=lambda x: x.get('vip', False), reverse=True)

                if not lista_anuncios:
                    st.warning("🧐 Nenhuma oferta encontrada para esta região.")
                else:
                    # Exibição em Grid (4 colunas)
                    cols = st.columns(4) 
                    for idx, anuncio in enumerate(lista_anuncios):
                        with cols[idx % 4]:
                            with st.container(border=True):
                                if anuncio.get('vip'):
                                    st.markdown("<span style='background:#FF4B4B; color:white; padding:2px 5px; border-radius:3px; font-size:10px;'>⭐ DESTAQUE</span>", unsafe_allow_html=True)
                                
                                f_capa = anuncio['fotos'][0] if anuncio.get('fotos') else (anuncio['foto'] if anuncio.get('foto') else "")
                                if f_capa: 
                                    st.image(f"data:image/jpeg;base64,{f_capa}", use_container_width=True)
                                else:
                                    st.markdown("<div style='height:150px; background:#222; display:flex; align-items:center; justify-content:center; border-radius:5px;'>📷 Sem Foto</div>", unsafe_allow_html=True)
                                
                                st.markdown(f"**{anuncio.get('titulo', 'Sem Título')}**")
                                st.markdown(f"<h4 style='color: #FF4B4B; margin-bottom: 0px;'>R$ {anuncio.get('preco', 0.0):.2f}</h4>", unsafe_allow_html=True)
                                
                                # --- CORREÇÃO: Exibição da Localização no Card ---
                                st.caption(f"📍 {anuncio.get('cidade')} - {anuncio.get('estado')}")
                                
                                if st.button("Ver Detalhes", key=f"vit_{anuncio['id']}", use_container_width=True):
                                    st.session_state['anuncio_detalhe'] = anuncio
                                    st.rerun()
        except Exception as e: 
            st.error(f"Erro ao carregar a vitrine VRS.")
            
    elif st.session_state['pagina_vrs'] in ["Anunciar", "Meus Anúncios"]:
        anuncios_vrs.exibir_painel_vendedor(db)
    elif st.session_state['pagina_vrs'] == "Chat":
        chat.exibir_interface_chat(db)
    elif st.session_state['pagina_vrs'] == "Admin":
        admin_vrs.exibir_painel_admin_vrs(db)

    # Rodapé Padrão VRS
    interface_javendeu_vrs.exibir_rodape_vrs()