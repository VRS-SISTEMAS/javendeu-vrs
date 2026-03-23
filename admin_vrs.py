# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: admin_vrs.py (PAINEL ADMINISTRATIVO MASTER - RESTAURADO)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import datetime
import publicidade_clientes 

def exibir_painel_admin_vrs(db):
    """Interface administrativa mestre da VRS Soluções."""
    email_admin = "vrsolucoes.sistemas@gmail.com"
    if not st.session_state.get('logado') or st.session_state['usuario']['email'] != email_admin:
        st.error("🚫 ACESSO NEGADO.")
        return

    st.markdown(f"<h1 style='color: #FF4B4B;'>🛠️ Gestão Master - VRS SOLUÇÕES</h1>", unsafe_allow_html=True)
    
    # Métricas Reais do Banco
    c1, c2, c3 = st.columns(3)
    try:
        c1.metric("Anúncios Ativos", len(list(db.collection("anuncios").where("status", "==", "ativo").stream())))
        c2.metric("Membros", len(list(db.collection("usuarios").stream())))
        c3.metric("Banners", len(list(db.collection("publicidade").stream())))
    except: pass

    tab_anuncios, tab_usuarios, tab_pub = st.tabs(["📢 ANÚNCIOS", "👥 USUÁRIOS", "💰 BANNERS"])

    with tab_anuncios:
        st.subheader("Moderar Anúncios")
        anuncios = db.collection("anuncios").stream()
        for doc in anuncios:
            it = doc.to_dict()
            with st.container(border=True):
                st.write(f"**{it.get('titulo')}** | {it.get('vendedor_email')}")
                if st.button("🗑️ EXCLUIR", key=f"adm_del_{doc.id}"):
                    db.collection("anuncios").document(doc.id).delete()
                    st.rerun()

    with tab_usuarios:
        st.subheader("Membros da Plataforma")
        users = db.collection("usuarios").stream()
        for u_doc in users:
            u = u_doc.to_dict()
            if u.get('email') == email_admin: continue
            with st.container(border=True):
                st.write(f"👤 {u.get('nome')} | {u.get('email')}")
                if st.button("BANIR", key=f"adm_ban_{u.get('email')}"):
                    db.collection("usuarios").document(u.get('email')).delete()
                    st.rerun()

    with tab_pub:
        # Garante que a gestão de publicidade esteja integrada ao Admin
        publicidade_clientes.gerenciar_banners_vrs(db)