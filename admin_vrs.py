# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: admin_vrs.py (PAINEL DE CONTROLE TOTAL - COM PUBLICIDADE)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import datetime
import publicidade_clientes # Importação do novo módulo

def exibir_painel_admin_vrs(db):
    """
    Interface administrativa de alto nível.
    Permite gerenciar anúncios, usuários, denúncias e publicidade paga.
    """
    
    # --- TRAVA DE SEGURANÇA MESTRE (VRS SOLUÇÕES) ---
    email_admin = "vrsolucoes.sistemas@gmail.com"
    
    if not st.session_state.get('logado') or st.session_state['usuario']['email'] != email_admin:
        st.error("🚫 ACESSO NEGADO. Área restrita à administração VRS Soluções.")
        return

    st.markdown(f"<h1 style='color: #FF4B4B;'>🛠️ Painel Administrativo - VRS SOLUÇÕES</h1>", unsafe_allow_html=True)
    st.caption(f"Gestão Master: Vitor | {datetime.datetime.now().strftime('%d/%m/%Y')}")

    # --- MÉTRICAS RÁPIDAS ---
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

    # --- ABAS DE PODER ADMINISTRATIVO ---
    tab_anuncios, tab_usuarios, tab_denuncias, tab_pub = st.tabs(["📢 MODERAR ANÚNCIOS", "👥 GERIR USUÁRIOS", "🛡️ DENÚNCIAS", "💰 PUBLICIDADE"])

    # --- ABA 1: MODERAÇÃO DE ANÚNCIOS ---
    with tab_anuncios:
        st.subheader("Controle de Vitrine Nacional")
        busca_anuncio = st.text_input("🔍 Localizar anúncio (Título ou E-mail)", key="busca_adm_anuncio")
        anuncios = db.collection("anuncios").order_by("data_publicacao", direction="DESCENDING").stream()
        
        for doc in anuncios:
            it = doc.to_dict()
            if busca_anuncio.lower() in it.get('titulo', '').lower() or busca_anuncio.lower() in it.get('vendedor_email', '').lower():
                with st.container(border=True):
                    col_foto, col_txt, col_btns = st.columns([1, 3, 2])
                    with col_foto:
                        if it.get('fotos'): st.image(f"data:image/jpeg;base64,{it['fotos'][0]}", use_container_width=True)
                    with col_txt:
                        st.markdown(f"**{it.get('titulo')}**")
                        st.caption(f"Vendedor: {it.get('vendedor_nome')} | {it.get('vendedor_email')}")
                        st.markdown(f"Preço: R$ {it.get('preco', 0.0):.2f}")
                    with col_btns:
                        label_vip = "⚪ REMOVER VIP" if it.get('vip') else "⭐ DAR DESTAQUE"
                        if st.button(label_vip, key=f"vip_{doc.id}", use_container_width=True):
                            db.collection("anuncios").document(doc.id).update({"vip": not it.get('vip')})
                            st.rerun()
                        if st.button("🗑️ EXCLUIR", key=f"del_{doc.id}", use_container_width=True):
                            db.collection("anuncios").document(doc.id).delete()
                            st.rerun()

    # --- ABA 2: GESTÃO DE USUÁRIOS ---
    with tab_usuarios:
        st.subheader("Membros Cadastrados")
        users = db.collection("usuarios").stream()
        for u_doc in users:
            u = u_doc.to_dict()
            if u.get('email') == email_admin: continue
            with st.container(border=True):
                inf, act, dlt = st.columns([2, 1, 1])
                with inf:
                    st.markdown(f"👤 **{u.get('nome')}**")
                    st.caption(f"E-mail: {u.get('email')} | Status: {u.get('status_conta', 'ativo').upper()}")
                with act:
                    if u.get('status_conta', 'ativo') == "ativo":
                        if st.button("🚫 BLOQUEAR", key=f"blk_{u.get('email')}", use_container_width=True):
                            db.collection("usuarios").document(u.get('email')).update({"status_conta": "bloqueado"})
                            st.rerun()
                    else:
                        if st.button("✅ REATIVAR", key=f"act_{u.get('email')}", use_container_width=True):
                            db.collection("usuarios").document(u.get('email')).update({"status_conta": "ativo"})
                            st.rerun()
                with dlt:
                    if st.button("💀 BANIR", key=f"ban_{u.get('email')}", use_container_width=True):
                        db.collection("usuarios").document(u.get('email')).delete()
                        st.rerun()

    # --- ABA 3: DENÚNCIAS ---
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

    # --- ABA 4: GESTÃO DE PUBLICIDADE (O NOVO PODER) ---
    with tab_pub:
        publicidade_clientes.gerenciar_banners_vrs(db)