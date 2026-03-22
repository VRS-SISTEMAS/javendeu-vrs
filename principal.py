# =================================================================
# VRS SISTEMAS - JÁ VENDEU?
# MÓDULO: principal.py (VERSÃO BLINDADA COM PAINEL ADMIN VITOR)
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
import admin_vrs  # Novo módulo de gerenciamento exclusivo

importlib.reload(usuarios_vrs)
importlib.reload(anuncios_vrs)
importlib.reload(admin_vrs)

interface_javendeu_vrs.aplicar_estilo_vrs()
db = conexao.conectar_banco_vrs()

# CSS MESTRE (MANTIDO)
st.markdown("""
    <style>
    .moldura-foto-vrs { background-color: #0E1117; border: 1px solid #333; border-radius: 10px; height: 400px; display: flex; align-items: center; justify-content: center; overflow: hidden; }
    .moldura-foto-vrs img { max-height: 400px; max-width: 100%; object-fit: contain; }
    .ponto-online { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px; box-shadow: 0 0 8px #00FF00; }
    .status-online-vrs { color: #00FF00; font-weight: bold; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

if 'pagina_vrs' not in st.session_state: st.session_state['pagina_vrs'] = "Home"
if 'anuncio_detalhe' not in st.session_state: st.session_state['anuncio_detalhe'] = None

col_vazia, col_login = st.columns([8, 2])
with col_login:
    if db is not None: usuarios_vrs.gerenciar_acesso(db)

# Menu Lateral Padrão
interface_javendeu_vrs.obter_menu_lateral_vrs()

# --- TRAVA DE SEGURANÇA MESTRE: MENU ADMIN EXCLUSIVO DO VITOR ---
if st.session_state.get('logado') and st.session_state['usuario']['email'] == "vrsolucoes.sistemas@gmail.com":
    with st.sidebar:
        st.markdown("---")
        st.markdown("<h3 style='color: #FF4B4B;'>🛠️ GESTÃO VRS</h3>", unsafe_allow_html=True)
        if st.button("PAINEL ADMINISTRATIVO", key="btn_admin_vrs", use_container_width=True):
            st.session_state['pagina_vrs'] = "Admin"
            st.session_state['anuncio_detalhe'] = None
            st.rerun()

# --- DETALHES DO PRODUTO (MANTIDO) ---
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
        else:
            st.info("📷 Este anúncio não possui fotos.")

    with col_info:
        with st.container(border=True):
            st.markdown(f"<h1 style='color: #FF4B4B; margin:0;'>R$ {item.get('preco', 0.0):.2f}</h1>", unsafe_allow_html=True)
            v_nome = item.get('vendedor_nome', 'Usuário').split()[0].title()
            st.markdown(f"👤 **Vendedor:** {v_nome} | <span class='status-online-vrs'><span class='ponto-online'></span>ONLINE</span>", unsafe_allow_html=True)
            st.markdown(f"📍 **{item.get('cidade')} - {item.get('estado')}**")
            st.write(item.get('descricao'))
            if st.button("⬅️ VOLTAR"):
                st.session_state['anuncio_detalhe'] = None
                st.rerun()

# --- NAVEGAÇÃO DE PÁGINAS ---
else:
    if st.session_state['pagina_vrs'] == "Home":
        interface_javendeu_vrs.exibir_identidade_visual_vrs()
        st.markdown("---")
        
        st.subheader("🛍️ Vitrine de Ofertas")
        f1, f2, f3 = st.columns([2, 1, 2])
        cat_f = f1.selectbox("O que você procura?", ["Todas"] + categorias.obter_categorias_vrs())
        est_f = f2.selectbox("Estado", ["Brasil"] + anuncios_vrs.ESTADOS_BR)
        cid_f = f3.text_input("Cidade (opcional)", placeholder="Ex: Duque de Caxias").strip().title()

        try:
            if db:
                # Lógica de Vitrine: VIPs primeiro, depois os normais por data
                docs = db.collection("anuncios").where("status", "==", "ativo").stream()
                lista_anuncios = []
                for d in docs:
                    it = d.to_dict()
                    if (cat_f == "Todas" or it.get('categoria') == cat_f) and \
                       (est_f == "Brasil" or it.get('estado') == est_f) and \
                       (not cid_f or cid_f in it.get('cidade', '')):
                        lista_anuncios.append(it | {"id": d.id})

                # Ordenação manual: Quem é VIP fica no topo
                lista_anuncios = sorted(lista_anuncios, key=lambda x: x.get('vip', False), reverse=True)

                if not lista_anuncios:
                    st.warning("🧐 Nenhuma oferta encontrada.")
                else:
                    cols = st.columns(4) 
                    for idx, anuncio in enumerate(lista_anuncios):
                        with cols[idx % 4]:
                            # Estilo diferencial se for VIP
                            border_style = "2px solid #FF4B4B" if anuncio.get('vip') else "1px solid #333"
                            with st.container(border=True):
                                if anuncio.get('vip'):
                                    st.markdown("<span style='background:#FF4B4B; color:white; padding:2px 5px; border-radius:3px; font-size:10px;'>⭐ DESTAQUE</span>", unsafe_allow_html=True)
                                
                                f_capa = ""
                                if anuncio.get('fotos') and len(anuncio['fotos']) > 0:
                                    f_capa = anuncio['fotos'][0]
                                elif anuncio.get('foto'):
                                    f_capa = anuncio['foto']
                                
                                if f_capa: 
                                    st.image(f"data:image/jpeg;base64,{f_capa}", use_container_width=True)
                                else:
                                    st.markdown("<div style='height:150px; background:#222; display:flex; align-items:center; justify-content:center; border-radius:5px;'>📷 Sem Foto</div>", unsafe_allow_html=True)
                                
                                st.markdown(f"**{anuncio.get('titulo', 'Sem Título')}**")
                                st.markdown(f"<h4 style='color: #FF4B4B;'>R$ {anuncio.get('preco', 0.0):.2f}</h4>", unsafe_allow_html=True)
                                st.caption(f"📍 {anuncio.get('cidade', 'N/A')}")
                                
                                if st.button("Ver Detalhes", key=f"vit_{anuncio['id']}", use_container_width=True):
                                    st.session_state['anuncio_detalhe'] = anuncio
                                    st.rerun()
        except Exception as e: 
            st.error(f"Erro ao carregar vitrine.")
            
    elif st.session_state['pagina_vrs'] in ["Anunciar", "Meus Anúncios"]:
        anuncios_vrs.exibir_painel_vendedor(db)
    elif st.session_state['pagina_vrs'] == "Chat":
        chat.exibir_interface_chat(db)
    elif st.session_state['pagina_vrs'] == "Admin":
        admin_vrs.exibir_painel_admin_vrs(db) # Página de gestão do Vitor

    interface_javendeu_vrs.exibir_rodape_vrs()