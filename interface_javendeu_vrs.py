# =================================================================
# VRS Soluções
# JÁ VENDEU? - PLATAFORMA DE NEGÓCIOS RÁPIDOS
# MÓDULO: interface_javendeu_vrs.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# AJUSTE: STATUS ONLINE DO VENDEDOR NOS DETALHES + MANUTENÇÃO TOTAL
# =================================================================

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import usuarios_vrs
import categorias
import estados 

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="JÁ VENDEU? - Marketplace VRS", layout="wide", page_icon="💰")

# --- CONEXÃO FIREBASE ---
def conectar_banco_vrs():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate("vrs-solucoes-firebase-adminsdk.json")
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        st.error(f"Erro de Conexão VRS: {e}")
        return None

db = conectar_banco_vrs()
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
        margin-bottom: 15px; display: flex; transition: 0.3s; height: 140px; 
    }
    .olx-card:hover { border-color: #FF4B4B; background-color: #252833; }
    .olx-img-thumb { width: 180px; height: 140px; object-fit: cover; border-radius: 8px 0 0 8px; }
    .olx-info { padding: 15px; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; overflow: hidden; }

    .main-photo-container {
        width: 100%; height: 450px; background-color: #000; border-radius: 8px;
        display: flex; align-items: center; justify-content: center; overflow: hidden; border: 1px solid #30363D;
    }
    .main-photo-container img { max-width: 100%; max-height: 450px; object-fit: contain; }
    
    .msg-caixa { background: #262730; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #FF4B4B; }
    input, textarea, select { background-color: #262730 !important; color: white !important; border: 1px solid #4B4B4B !important; }
    .stButton>button { background-color: #FF4B4B !important; color: white !important; border-radius: 5px; font-weight: bold; }
    
    /* STATUS ONLINE */
    .vrs-online { color: #00FF00; font-weight: bold; font-size: 14px; }
    .vrs-offline { color: #888888; font-weight: bold; font-size: 14px; }

    .footer-vrs { background-color: #1A1C24; padding: 20px; border-radius: 10px; border-top: 3px solid #FF4B4B; margin-top: 50px; text-align: center; }
    .footer-warning { color: #FF4B4B; font-weight: bold; font-size: 16px; }

    .watermark { position: fixed; bottom: 10px; right: 15px; font-size: 10px; color: #444; z-index: 100; }
    </style>
    <div class="watermark">VRS Soluções</div>
    """, unsafe_allow_html=True)

# --- HEADER ---
header_col1, header_col2, header_col3 = st.columns([1, 2, 1])
with header_col2:
    st.markdown("<div class='logo-container'><h1 class='main-title'>JÁ VENDEU?</h1><p class='impact-phrase'>Anuncie agora e transforme desapego em lucro rápido!</p></div>", unsafe_allow_html=True)
with header_col3:
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    esta_logado = usuarios_vrs.gerenciar_acesso(db)

st.markdown("---")
menu = st.sidebar.radio("Navegação", ["🛍️ Ver Ofertas", "➕ Anunciar Agora", "🗂️ Meus Anúncios", "💬 Chat Interno"])

# --- ABA: CHAT ---
if menu == "💬 Chat Interno":
    if not esta_logado: st.warning("⚠️ Faça login.")
    else:
        st.subheader("💬 Minhas Mensagens")
        email_atual = st.session_state['usuario']['email']
        try:
            msgs = db.collection("mensagens").where("participantes", "array_contains", email_atual).order_by("data", direction=firestore.Query.DESCENDING).stream()
            for m in msgs:
                d = m.to_dict()
                st.markdown(f"<div class='msg-caixa'><b>{d['remetente_nome']}</b> sobre <i>{d['anuncio_nome']}</i>:<br>{d['texto']}</div>", unsafe_allow_html=True)
        except:
            msgs = db.collection("mensagens").where("participantes", "array_contains", email_atual).stream()
            for m in msgs:
                d = m.to_dict()
                st.markdown(f"<div class='msg-caixa'><b>{d['remetente_nome']}</b>: {d['texto']}</div>", unsafe_allow_html=True)

# --- ABA: ANUNCIAR ---
elif menu == "➕ Anunciar Agora":
    if not esta_logado: st.warning("⚠️ Faça login.")
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
            st.write("🖼️ **Links das Fotos**")
            f1 = st.text_input("Foto 1 (Principal)")
            f2 = st.text_input("Foto 2")
            
            st.info("⚠️ **Termos de Uso:** Proibido o uso de imagens abusivas, impróprias ou ilegais. O 'JÁ VENDEU?' atua apenas como vitrine publicitária. Não nos responsabilizamos por negociações.")
            aceite = st.checkbox("Eu li e aceito que sou o único responsável pela veracidade e ética deste anúncio.")

            if st.form_submit_button("🚀 PUBLICAR"):
                if aceite and nome and preco > 0 and f1:
                    db.collection("anuncios").add({
                        "nome": nome, "categoria": cat, "valor": preco, "zap": whatsapp,
                        "estado": uf, "local": cid, "desc": desc, "fotos": [f for f in [f1, f2] if f],
                        "data": datetime.datetime.now(), "status": "ativo",
                        "email_dono": st.session_state['usuario']['email'],
                        "nome_dono": st.session_state['usuario']['nome']
                    })
                    st.success("Anunciado com sucesso!")
                    st.rerun()
                elif not aceite:
                    st.error("Você precisa aceitar os termos para publicar.")

# --- ABA: MEUS ANÚNCIOS ---
elif menu == "🗂️ Meus Anúncios":
    if not esta_logado: st.warning("⚠️ Faça login.")
    else:
        docs = db.collection("anuncios").where("email_dono", "==", st.session_state['usuario']['email']).stream()
        for doc in docs:
            it = doc.to_dict()
            foto_c = it.get('fotos', [it.get('foto', 'https://via.placeholder.com/150')])[0]
            col_inf, col_btn = st.columns([4, 1.5])
            with col_inf:
                st.markdown(f"<div class='olx-card'><img src='{foto_c}' class='olx-img-thumb'><div class='olx-info'><b>{it['nome']}</b></div></div>", unsafe_allow_html=True)
            with col_btn:
                st.write("<br>")
                if st.button("🗑️ EXCLUIR", key=f"d_{doc.id}", use_container_width=True):
                    db.collection("anuncios").document(doc.id).delete()
                    st.rerun()

# --- ABA: VITRINE ---
elif menu == "🛍️ Ver Ofertas":
    c_f1, c_f2 = st.columns(2)
    with c_f1: filtro_cat = st.selectbox("📂 Categorias", lista_cats)
    with c_f2: filtro_uf = st.selectbox("📍 Estado", lista_filtro_ufs)
    busca = st.text_input("🔍 O que você procura?")
    
    if 'detalhe_id' in st.session_state:
        doc = db.collection("anuncios").document(st.session_state.detalhe_id).get()
        it = doc.to_dict()
        if st.button("⬅️ Voltar"):
            del st.session_state.detalhe_id
            st.rerun()
        
        c_th, c_img = st.columns([0.5, 3])
        gal = it.get('fotos', [it.get('foto', 'https://via.placeholder.com/400')])
        if 'foto_index' not in st.session_state: st.session_state.foto_index = 0
        with c_th:
            for idx, lk in enumerate(gal):
                if st.button(f"📸 {idx+1}", key=f"b_{idx}", use_container_width=True):
                    st.session_state.foto_index = idx
                    st.rerun()
        with c_img: st.markdown(f"<div class='main-photo-container'><img src='{gal[st.session_state.foto_index]}'></div>", unsafe_allow_html=True)

        # --- CONSULTA STATUS DO VENDEDOR ---
        vendedor_ref = db.collection("usuarios").document(it['email_dono']).get()
        v_info = vendedor_ref.to_dict() if vendedor_ref.exists else {}
        is_online = v_info.get('status_vrs') == 'online'
        status_html = "<span class='vrs-online'>🟢 Online agora</span>" if is_online else "<span class='vrs-offline'>⚪ Offline</span>"

        st.title(it['nome'])
        st.markdown(status_html, unsafe_allow_html=True)
        st.header(f"R$ {it['valor']:,.2f}")
        st.write(f"📍 {it.get('local', '')} - {it.get('estado', '')}")
        st.write(f"👤 Vendedor: {it.get('nome_dono', 'Não informado')}")
        st.write(it['desc'])
        
        pode_ver_zap = usuarios_vrs.verificar_privacidade(it['email_dono'], db)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💬 ENVIAR MENSAGEM", use_container_width=True):
                if not esta_logado: st.error("Logue primeiro!")
                else: st.session_state.abrir_chat = True
        with c2:
            if pode_ver_zap: st.success(f"📱 WhatsApp: {it.get('zap')}")
            else: st.info("🔒 Vendedor atende apenas pelo Chat.")

        if st.session_state.get("abrir_chat"):
            with st.form("msg_vrs"):
                txt = st.text_area("Sua mensagem:")
                if st.form_submit_button("ENVIAR"):
                    db.collection("mensagens").add({
                        "anuncio_id": doc.id, "anuncio_nome": it['nome'],
                        "remetente_email": st.session_state['usuario']['email'],
                        "remetente_nome": st.session_state['usuario']['nome'],
                        "participantes": [st.session_state['usuario']['email'], it['email_dono']],
                        "texto": txt, "data": datetime.datetime.now()
                    })
                    st.success("Enviada!")
                    del st.session_state.abrir_chat
    else:
        query = db.collection("anuncios").where("status", "==", "ativo")
        query = categorias.filtrar_por_categoria(query, filtro_cat)
        if filtro_uf != "Todos": query = query.where("estado", "==", filtro_uf)
        
        resultados = [doc for doc in query.stream() if busca.lower() in doc.to_dict().get('nome', '').lower()]
        
        if not resultados:
            st.markdown("<h3 style='text-align: center; color: #888;'>🔍 Busca não encontrada para este filtro.</h3>", unsafe_allow_html=True)
        else:
            for doc in resultados:
                it = doc.to_dict()
                foto_v = it.get('fotos', [it.get('foto', 'https://via.placeholder.com/200')])[0]
                st.markdown(f"<div class='olx-card'><img src='{foto_v}' class='olx-img-thumb'><div class='olx-info'><b>{it['nome']}</b><br>R$ {it['valor']:,.2f}<br><small>{it.get('local', '')} - {it.get('estado', '')}</small></div></div>", unsafe_allow_html=True)
                if st.button("Detalhes", key=f"det_{doc.id}"):
                    st.session_state.detalhe_id = doc.id
                    st.rerun()

# --- RODAPÉ DE SEGURANÇA ---
st.markdown("""
    <div class='footer-vrs'>
        <p class='footer-warning'>🛡️ SEGURANÇA VRS SOLUÇÕES</p>
        <p>Ao negociar, priorize sua segurança: procure sempre locais movimentados como <b>shoppings, estações de trem/metrô ou postos de gasolina</b> com fluxo de pessoas. Nunca faça depósitos antecipados sem ver o produto.</p>
        <p style='font-size: 12px; color: #888;'>© 2026 JÁ VENDEU? - A sua vitrine de negócios rápidos.</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 JÁ VENDEU? | Sistemas VRS Soluções")