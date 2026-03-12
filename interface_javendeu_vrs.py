# =================================================================
# VRS Soluções
# JÁ VENDEU? - PLATAFORMA DE NEGÓCIOS RÁPIDOS
# MÓDULO: interface_javendeu_vrs.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# AJUSTE: CORREÇÃO DEFINITIVA DE CONEXÃO E LIMPEZA DE INTERFACE
# =================================================================

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import os
import usuarios_vrs
import categorias
import estados 

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="JÁ VENDEU? - Marketplace VRS", layout="wide", page_icon="💰")

# --- CONEXÃO FIREBASE (BLINDAGEM TOTAL VRS) ---
@st.cache_resource
def conectar_banco_vrs():
    """Realiza a conexão segura com o Firestore da VRS Soluções."""
    try:
        if not firebase_admin._apps:
            # 1. TENTA VIA SECRETS (PARA DEPLOY NO STREAMLIT CLOUD)
            if "textkey" in st.secrets:
                cred_dict = dict(st.secrets["textkey"])
                
                # TRATAMENTO AVANÇADO DA CHAVE PRIVADA
                if "private_key" in cred_dict:
                    # Garante que as quebras de linha sejam interpretadas corretamente
                    p_key = cred_dict["private_key"].replace("\\n", "\n")
                    # Remove eventuais aspas extras que o TOML pode inserir
                    p_key = p_key.strip().strip('"').strip("'")
                    cred_dict["private_key"] = p_key
                
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
            
            # 2. TENTA VIA ARQUIVO (PARA USO EM PC LOCAL)
            else:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                path_json = os.path.join(base_dir, "vrs-solucoes-firebase-adminsdk.json")
                if os.path.exists(path_json):
                    cred = credentials.Certificate(path_json)
                    firebase_admin.initialize_app(cred)
                else:
                    st.error("Erro Crítico: Configure os Secrets no painel do Streamlit ou adicione o JSON.")
                    return None
                    
        return firestore.client()
    except Exception as e:
        st.error(f"Erro de Conexão Segura VRS: {e}")
        return None

# Inicializa o banco de dados oficial
db = conectar_banco_vrs()

# Carrega listas auxiliares dos módulos VRS
lista_cats = categorias.obter_categorias_vrs()
lista_ufs = estados.obter_estados_vrs()
lista_filtro_ufs = estados.obter_estados_com_todos_vrs()

# --- ESTILO CSS PROFISSIONAL (VRS SOLUÇÕES) ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .logo-container { text-align: center; width: 100%; padding: 20px 0 5px 0; }
    .main-title { color: #FF4B4B; font-weight: 900; font-size: 65px; margin-bottom: 0px; text-shadow: 2px 2px #000; }
    .impact-phrase { color: #AAAAAA; font-size: 20px; font-weight: 500; font-style: italic; margin-top: -10px; margin-bottom: 25px; }
    
    .olx-card {
        background-color: #1A1C24; border-radius: 8px; border: 1px solid #30363D;
        margin-bottom: 15px; display: flex; transition: 0.3s; height: 140px; overflow: hidden;
    }
    .olx-card:hover { border-color: #FF4B4B; background-color: #252833; }
    .olx-img-thumb { width: 180px; height: 140px; object-fit: cover; border-radius: 8px 0 0 8px; }
    .olx-info { padding: 15px; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; }

    .main-photo-container {
        width: 100%; height: 450px; background-color: #000; border-radius: 8px;
        display: flex; align-items: center; justify-content: center; overflow: hidden; border: 1px solid #30363D;
    }
    .main-photo-container img { max-width: 100%; max-height: 450px; object-fit: contain; }
    
    .msg-caixa { background: #262730; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #FF4B4B; }
    .vrs-online { color: #00FF00; font-weight: bold; font-size: 14px; }
    .vrs-offline { color: #888888; font-weight: bold; font-size: 14px; }
    .footer-vrs { background-color: #1A1C24; padding: 20px; border-radius: 10px; border-top: 3px solid #FF4B4B; margin-top: 50px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
header_col1, header_col2, header_col3 = st.columns([1, 2, 1])
with header_col2:
    st.markdown("<div class='logo-container'><h1 class='main-title'>JÁ VENDEU?</h1><p class='impact-phrase'>Transforme desapego em lucro rápido!</p></div>", unsafe_allow_html=True)
with header_col3:
    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
    if db:
        esta_logado = usuarios_vrs.gerenciar_acesso(db)
    else:
        esta_logado = False

st.markdown("---")
menu = st.sidebar.radio("Navegação", ["🛍️ Ver Ofertas", "➕ Anunciar Agora", "🗂️ Meus Anúncios", "💬 Chat Interno"])

# --- ABA: CHAT ---
if menu == "💬 Chat Interno":
    if not esta_logado: 
        st.warning("⚠️ Faça login para ver suas mensagens.")
    else:
        st.subheader("💬 Minhas Mensagens")
        email_atual = st.session_state['usuario']['email']
        try:
            # Busca mensagens onde o usuário participa
            msgs = db.collection("mensagens").where("participantes", "array_contains", email_atual).stream()
            cont_msg = 0
            for m in msgs:
                d = m.to_dict()
                st.markdown(f"<div class='msg-caixa'><b>{d.get('remetente_nome', 'Usuário')}</b> sobre <i>{d.get('anuncio_nome', 'Produto')}</i>:<br>{d.get('texto', '')}</div>", unsafe_allow_html=True)
                cont_msg += 1
            if cont_msg == 0:
                st.info("Nenhuma mensagem por enquanto.")
        except Exception:
            st.error("Erro ao carregar mensagens.")

# --- ABA: ANUNCIAR ---
elif menu == "➕ Anunciar Agora":
    if not esta_logado: 
        st.warning("⚠️ Faça login para anunciar.")
    else:
        st.subheader("📢 Criar Novo Anúncio")
        with st.form("form_venda_vrs", clear_on_submit=True):
            nome = st.text_input("Título do Produto")
            cat = st.selectbox("Categoria", lista_cats[1:])
            desc = st.text_area("Descrição detalhada")
            c1, c2, c3 = st.columns([1, 2, 2])
            with c1: uf = st.selectbox("UF", lista_ufs, index=lista_ufs.index("RJ"))
            with c2: cid = st.text_input("Cidade / Bairro")
            with c3: preco = st.number_input("Preço (R$)", min_value=0.0)
            whatsapp = st.text_input("WhatsApp", value=st.session_state['usuario']['zap'])
            f1 = st.text_input("Foto 1 (Principal - Link)")
            f2 = st.text_input("Foto 2 (Link)")
            aceite = st.checkbox("Aceito os termos de uso e veracidade.")

            if st.form_submit_button("🚀 PUBLICAR"):
                if aceite and nome and preco > 0 and f1:
                    try:
                        db.collection("anuncios").add({
                            "nome": nome, "categoria": cat, "valor": preco, "zap": whatsapp,
                            "estado": uf, "local": cid, "desc": desc, "fotos": [f for f in [f1, f2] if f],
                            "data": datetime.datetime.now(), "status": "ativo",
                            "email_dono": st.session_state['usuario']['email'],
                            "nome_dono": st.session_state['usuario']['nome']
                        })
                        st.success("Anunciado com sucesso!")
                        st.rerun()
                    except Exception: 
                        st.error("Erro ao publicar.")
                else: 
                    st.error("Preencha os campos obrigatórios e aceite os termos.")

# --- ABA: MEUS ANÚNCIOS ---
elif menu == "🗂️ Meus Anúncios":
    if not esta_logado: 
        st.warning("⚠️ Faça login para gerenciar seus anúncios.")
    else:
        try:
            docs = db.collection("anuncios").where("email_dono", "==", st.session_state['usuario']['email']).stream()
            for doc in docs:
                it = doc.to_dict()
                foto_c = it.get('fotos', ['https://via.placeholder.com/150'])[0]
                col_inf, col_btn = st.columns([4, 1.5])
                with col_inf:
                    st.markdown(f"<div class='olx-card'><img src='{foto_c}' class='olx-img-thumb'><div class='olx-info'><b>{it['nome']}</b><br>R$ {it['valor']:,.2f}</div></div>", unsafe_allow_html=True)
                with col_btn:
                    st.write("<br>")
                    if st.button("🗑️ EXCLUIR", key=f"d_{doc.id}", use_container_width=True):
                        db.collection("anuncios").document(doc.id).delete()
                        st.rerun()
        except Exception: 
            st.info("Nenhum anúncio encontrado.")

# --- ABA: VITRINE ---
elif menu == "🛍️ Ver Ofertas":
    c_f1, c_f2 = st.columns(2)
    with c_f1: filtro_cat = st.selectbox("📂 Categorias", lista_cats)
    with c_f2: filtro_uf = st.selectbox("📍 Estado", lista_filtro_ufs)
    busca = st.text_input("🔍 O que você procura?")
    
    if 'detalhe_id' in st.session_state:
        # VISUALIZAÇÃO DETALHADA DO PRODUTO
        doc = db.collection("anuncios").document(st.session_state.detalhe_id).get()
        if doc.exists:
            it = doc.to_dict()
            if st.button("⬅️ Voltar"):
                del st.session_state.detalhe_id
                st.rerun()
            
            c_th, c_img = st.columns([0.5, 3])
            gal = it.get('fotos', ['https://via.placeholder.com/400'])
            if 'foto_index' not in st.session_state: st.session_state.foto_index = 0
            with c_th:
                for idx, lk in enumerate(gal):
                    if st.button(f"📸 {idx+1}", key=f"b_{idx}", use_container_width=True):
                        st.session_state.foto_index = idx
                        st.rerun()
            with c_img: 
                st.markdown(f"<div class='main-photo-container'><img src='{gal[st.session_state.foto_index]}'></div>", unsafe_allow_html=True)

            st.title(it['nome'])
            st.header(f"R$ {it['valor']:,.2f}")
            st.write(f"📍 {it.get('local', '')} - {it.get('estado', '')}")
            st.write(f"👤 Vendedor: {it.get('nome_dono', 'VRS Usuário')}")
            st.info(it.get('desc', 'Sem descrição.'))
            
            pode_ver_zap = usuarios_vrs.verificar_privacidade(it['email_dono'], db)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("💬 ENVIAR MENSAGEM", use_container_width=True):
                    if not esta_logado: st.error("Logue primeiro!")
                    else: st.success("Função de chat em breve!")
            with c2:
                if pode_ver_zap: 
                    st.success(f"📱 WhatsApp: {it.get('zap')}")
                else: 
                    st.info("🔒 Vendedor atende apenas pelo Chat.")
    else:
        # LISTAGEM DE CARDS
        try:
            query = db.collection("anuncios").where("status", "==", "ativo")
            query = categorias.filtrar_por_categoria(query, filtro_cat)
            if filtro_uf != "Todos": 
                query = query.where("estado", "==", filtro_uf)
            
            resultados = [doc for doc in query.stream() if busca.lower() in doc.to_dict().get('nome', '').lower()]
            if not resultados:
                st.markdown("<h3 style='text-align: center; color: #888;'>🔍 Nada encontrado.</h3>", unsafe_allow_html=True)
            else:
                for doc in resultados:
                    it = doc.to_dict()
                    foto_v = it.get('fotos', ['https://via.placeholder.com/200'])[0]
                    st.markdown(f"<div class='olx-card'><img src='{foto_v}' class='olx-img-thumb'><div class='olx-info'><b>{it['nome']}</b><br>R$ {it['valor']:,.2f}<br><small>{it.get('local', '')} - {it.get('estado', '')}</small></div></div>", unsafe_allow_html=True)
                    if st.button("Detalhes", key=f"det_{doc.id}"):
                        st.session_state.detalhe_id = doc.id
                        st.rerun()
        except Exception: 
            st.info("Carregando vitrine...")

# --- RODAPÉ ---
st.markdown("<div class='footer-vrs'><p>🛡️ Segurança VRS: Nunca pague antes de ver o produto!</p></div>", unsafe_allow_html=True)
st.sidebar.caption("© 2026 JÁ VENDEU? | VRS Soluções")