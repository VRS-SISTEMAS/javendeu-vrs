# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: admin_vrs.py (PAINEL DE CONTROLE TOTAL DO VITOR)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import datetime

def exibir_painel_admin_vrs(db):
    """
    Interface administrativa de alto nível.
    Permite gerenciar anúncios, denúncias e usuários da rede VRS.
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
    tab_anuncios, tab_usuarios, tab_denuncias = st.tabs(["📢 MODERAR ANÚNCIOS", "👥 GERIR USUÁRIOS", "🛡️ DENÚNCIAS"])

    # --- ABA 1: MODERAÇÃO DE ANÚNCIOS (Limpeza de "anúncios bobos") ---
    with tab_anuncios:
        st.subheader("Controle de Vitrine Nacional")
        busca_anuncio = st.text_input("🔍 Localizar anúncio (Título ou E-mail)", key="busca_adm_anuncio")
        
        anuncios = db.collection("anuncios").order_by("data_publicacao", direction="DESCENDING").stream()
        
        for doc in anuncios:
            it = doc.to_dict()
            anuncio_id = doc.id
            vendedor = it.get('vendedor_email', '').lower()
            titulo = it.get('titulo', '').lower()

            # Filtro de busca para facilitar a vida do Vitor
            if busca_anuncio.lower() in titulo or busca_anuncio.lower() in vendedor:
                with st.container(border=True):
                    col_foto, col_txt, col_btns = st.columns([1, 3, 2])
                    
                    with col_foto:
                        if it.get('fotos'):
                            st.image(f"data:image/jpeg;base64,{it['fotos'][0]}", use_container_width=True)
                    
                    with col_txt:
                        st.markdown(f"**{it.get('titulo')}**")
                        st.caption(f"Vendedor: {it.get('vendedor_nome')} | {it.get('vendedor_email')}")
                        st.markdown(f"Preço: R$ {it.get('preco', 0.0):.2f}")
                        if it.get('vip'): st.markdown("⭐ **DESTAQUE VIP ATIVO**")
                    
                    with col_btns:
                        # Gestão de Destaque
                        label_vip = "⚪ REMOVER VIP" if it.get('vip') else "⭐ DAR DESTAQUE"
                        if st.button(label_vip, key=f"vip_{anuncio_id}", use_container_width=True):
                            db.collection("anuncios").document(anuncio_id).update({"vip": not it.get('vip')})
                            st.rerun()

                        # Exclusão de anúncio bobo/indesejado
                        if st.button("🗑️ EXCLUIR ANÚNCIO", key=f"del_anuncio_{anuncio_id}", use_container_width=True):
                            db.collection("anuncios").document(anuncio_id).delete()
                            st.success("Anúncio removido!")
                            st.rerun()

    # --- ABA 2: GESTÃO DE USUÁRIOS (Bloquear e Excluir) ---
    with tab_usuarios:
        st.subheader("Membros Cadastrados")
        users = db.collection("usuarios").stream()
        
        for u_doc in users:
            u = u_doc.to_dict()
            u_email = u.get('email')
            u_status = u.get('status_conta', 'ativo')
            
            # Pula o administrador para evitar auto-bloqueio
            if u_email == email_admin: continue

            with st.container(border=True):
                inf, act, dlt = st.columns([2, 1, 1])
                with inf:
                    st.markdown(f"👤 **{u.get('nome')}**")
                    st.caption(f"E-mail: {u_email} | Zap: {u.get('whatsapp')}")
                    cor_status = "red" if u_status == "bloqueado" else "#00FF00"
                    st.markdown(f"Status: <span style='color:{cor_status};'>{u_status.upper()}</span>", unsafe_allow_html=True)
                
                with act:
                    # Alterna entre Bloquear e Desbloquear
                    if u_status == "ativo":
                        if st.button("🚫 BLOQUEAR", key=f"blk_{u_email}", use_container_width=True):
                            db.collection("usuarios").document(u_email).update({"status_conta": "bloqueado"})
                            st.rerun()
                    else:
                        if st.button("✅ REATIVAR", key=f"act_{u_email}", use_container_width=True):
                            db.collection("usuarios").document(u_email).update({"status_conta": "ativo"})
                            st.rerun()
                            
                with dlt:
                    # Exclusão permanente do usuário e seus rastros
                    if st.button("💀 BANIR", key=f"ban_{u_email}", use_container_width=True):
                        # Deleta o usuário
                        db.collection("usuarios").document(u_email).delete()
                        # Limpa os anúncios dele para não deixar lixo no site
                        meus_anuncios = db.collection("anuncios").where("vendedor_email", "==", u_email).stream()
                        for a in meus_anuncios:
                            db.collection("anuncios").document(a.id).delete()
                        st.error(f"Usuário {u_email} banido da rede VRS!")
                        st.rerun()

    # --- ABA 3: DENÚNCIAS ---
    with tab_denuncias:
        st.subheader("Alertas de Segurança Recebidos")
        denuncias = db.collection("denuncias").order_by("data", direction="DESCENDING").stream()
        
        for den in denuncias:
            d = den.to_dict()
            with st.container(border=True):
                st.warning(f"🚨 Denúncia: {d.get('titulo')}")
                st.write(f"Vendedor sob suspeita: {d.get('vendedor_email', 'Não informado')}")
                st.caption(f"Reportado por: {d.get('denunciante')} em {d.get('data')}")
                if st.button("OK, RESOLVIDO", key=f"den_ok_{den.id}"):
                    db.collection("denuncias").document(den.id).delete()
                    st.rerun()