# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: publicidade_clientes.py (FIX DO BANNER)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime

def gerenciar_banners_vrs(db):
    st.subheader("🚀 Gestão de Banners")
    with st.expander("➕ Novo Banner"):
        with st.form("f_banner", clear_on_submit=True):
            cliente = st.text_input("Cliente")
            link = st.text_input("Link WhatsApp/Site")
            uf = st.selectbox("Estado", ["Brasil", "SP", "RJ", "MG", "PR", "RS", "SC"])
            arq = st.file_uploader("Banner (1200x200)", type=['png', 'jpg'])
            if st.form_submit_button("ATIVAR"):
                if cliente and link and arq:
                    img = base64.b64encode(arq.getvalue()).decode('utf-8')
                    db.collection("publicidade").add({
                        "cliente": cliente, "link": link, "estado_alvo": uf,
                        "foto": img, "data": datetime.datetime.now()
                    })
                    st.success("No ar!")
                    st.rerun()

    banners = db.collection("publicidade").stream()
    for b in banners:
        d = b.to_dict()
        with st.container(border=True):
            st.image(f"data:image/jpeg;base64,{d['foto']}", width=200)
            if st.button("🗑️ Remover", key=f"del_{b.id}"):
                db.collection("publicidade").document(b.id).delete()
                st.rerun()

def exibir_banner_rotativo_vrs(db, estado_atual="Brasil"):
    try:
        filtros = ["Brasil"]
        if estado_atual != "Brasil": filtros.append(estado_atual)
        query = db.collection("publicidade").where("estado_alvo", "in", filtros).stream()
        lista = [b.to_dict() for b in query]
        if lista:
            banner = lista[-1]
            st.markdown(f"""
                <div class="vrs-banner-fix">
                    <a href="{banner['link']}" target="_blank">
                        <img src="data:image/jpeg;base64,{banner['foto']}" style="width:100%; border-radius:10px;">
                    </a>
                </div>
            """, unsafe_allow_html=True)
    except: pass