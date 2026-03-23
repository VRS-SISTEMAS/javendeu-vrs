# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: publicidade_clientes.py (SISTEMA DE BANNERS)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime

def gerenciar_banners_vrs(db):
    """Painel para o Vitor cadastrar publicidade paga."""
    st.subheader("🚀 Gestão de Banners")
    with st.expander("➕ Novo Banner de Cliente"):
        with st.form("f_banner_vrs", clear_on_submit=True):
            cliente = st.text_input("Nome do Cliente")
            link = st.text_input("Link WhatsApp/Site (com https://)")
            uf = st.selectbox("Estado Alvo", ["Brasil", "SP", "RJ", "MG", "PR", "RS", "SC", "BA", "PE", "CE"])
            arq = st.file_uploader("Upload do Banner", type=['png', 'jpg', 'jpeg'])
            if st.form_submit_button("ATIVAR PUBLICIDADE"):
                if cliente and link and arq:
                    img = base64.b64encode(arq.getvalue()).decode('utf-8')
                    db.collection("publicidade").add({
                        "cliente": cliente, "link": link, "estado_alvo": uf,
                        "foto": img, "data": datetime.datetime.now()
                    })
                    st.success("Banner ativado com sucesso!")
                    st.rerun()

    banners = db.collection("publicidade").stream()
    for b in banners:
        d = b.to_dict()
        with st.container(border=True):
            st.image(f"data:image/jpeg;base64,{d['foto']}", width=300)
            st.write(f"Cliente: {d['cliente']} | Estado: {d['estado_alvo']}")
            if st.button("🗑️ Remover Banner", key=f"del_pub_{b.id}"):
                db.collection("publicidade").document(b.id).delete()
                st.rerun()

def exibir_banner_rotativo_vrs(db, estado_atual="Brasil"):
    """Exibe o banner no topo da vitrine."""
    try:
        filtros = ["Brasil"]
        if estado_atual != "Brasil": filtros.append(estado_atual)
        query = db.collection("publicidade").where("estado_alvo", "in", filtros).stream()
        lista = [b.to_dict() for b in query]
        if lista:
            banner = lista[-1]
            st.markdown(f"""
                <div style="width:100%; margin-bottom: 20px;">
                    <a href="{banner['link']}" target="_blank">
                        <img src="data:image/jpeg;base64,{banner['foto']}" style="width:100%; border-radius:10px; border: 1px solid #333;">
                    </a>
                </div>
            """, unsafe_allow_html=True)
    except Exception as e: pass