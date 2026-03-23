# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: admin_vrs.py (PAINEL DE CONTROLE TOTAL)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import datetime
import publicidade_clientes 

def exibir_painel_admin_vrs(db):
    """Interface administrativa para gestão total da plataforma."""
    
    email_admin = "vrsolucoes.sistemas@gmail.com"
    
    if not st.session_state.get('logado') or st.session_state['usuario']['email'] != email_admin:
        st.error("🚫 ACESSO NEGADO. Área restrita à administração VRS Soluções.")
        return

    st.markdown(f"<h1 style='color: #FF4B4B;'>🛠️ Painel Administrativo - VRS SOLUÇÕES</h1>", unsafe_allow_html=True)
    st.caption(f"Gestão Master: Vitor | {datetime.datetime.now().strftime('%d/%m/%Y')}")

    st.markdown("### 📊 Visão Geral da Rede")
    c1, c2, c3 = st.columns(3)
    
    try:
        total_anuncios = len(list(db.collection("anuncios").stream()))
        total_usuarios = len(list(db.collection("usuarios").stream()))
        total_denuncias = len(list(db.collection("denuncias").stream()))
        
        c1.metric("Anúncios no Ar", total_anuncios)
        c2.metric("Membros Ativos", total_usuarios)
        c3.metric("Denúncias", total_denuncias)
    except:
        st.warning("Aguardando sincronização de métricas...")

    st.markdown("---")

    tab_anuncios, tab_usuarios, tab_denuncias, tab_pub = st.tabs(["📢 MODERAR ANÚNCIOS", "👥 GERIR USUÁRIOS", "🛡️ DENÚNCIAS", "💰 PUBLICIDADE"])

    with tab_anuncios:
        st.subheader("Controle de Vitrine Nacional")
        busca_anuncio = st.text_input("🔍 Localizar anúncio", key="busca_adm_anuncio")
        anuncios = db.collection("anuncios").order_by("data_publicacao", direction="DESCENDING").stream()
        
        for doc in anuncios:
            it = doc.to_dict()
            if busca_anuncio.lower() in it.get('titulo', '').lower():
                with st.container(border=True):
                    col_foto, col_txt, col_btns = st.columns([1, 3, 2])
                    with col_foto:
                        if it.get('fotos'): st.image(f"data:image/jpeg;base64,{it['fotos'][0]}", use_container_width=True)
                    with col_txt:
                        st.markdown(f"**{it.get('titulo')}**")
                        st.caption(f"Vendedor: {it.get('vendedor_email')}")
                    with col_btns:
                        if st.button("🗑️ EXCLUIR", key=f"del_{doc.id}", use_container_width=True):
                            db.collection("anuncios").document(doc.id).delete()
                            st.rerun()

    with tab_usuarios:
        st.subheader("Membros Cadastrados")
        users = db.collection("usuarios").stream()
        for u_doc in users:
            u = u_doc.to_dict()
            if u.get('email') == email_admin: continue
            with st.container(border=True):
                st.markdown(f"👤 **{u.get('nome')}** ({u.get('email')})")
                if st.button("💀 BANIR", key=f"ban_{u.get('email')}"):
                    db.collection("usuarios").document(u.get('email')).delete()
                    st.rerun()

    with tab_denuncias:
        st.subheader("Alertas de Segurança")
        denuncias = db.collection("denuncias").stream()
        for den in denuncias:
            d = den.to_dict()
            with st.container(border=True):
                st.warning(f"🚨 Denúncia: {d.get('titulo')}")
                if st.button("RESOLVIDO", key=f"den_{den.id}"):
                    db.collection("denuncias").document(den.id).delete()
                    st.rerun()

    with tab_pub:
        publicidade_clientes.gerenciar_banners_vrs(db)