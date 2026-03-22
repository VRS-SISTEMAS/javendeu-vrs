# =================================================================
# VRS SISTEMAS - JÁ VENDEU?
# MÓDULO: admin_vrs.py (PAINEL DE CONTROLE EXCLUSIVO DO VITOR)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import datetime

def exibir_painel_admin_vrs(db):
    """Painel secreto de gerenciamento da plataforma JÁ VENDEU?."""
    
    # --- TRAVA DE SEGURANÇA MESTRE ---
    # Somente o e-mail do Vitor tem acesso a este código
    email_admin = "vrsolucoes.sistemas@gmail.com"
    
    if not st.session_state.get('logado') or st.session_state['usuario']['email'] != email_admin:
        st.error("🚫 ACESSO NEGADO. Área restrita à administração VRS Soluções.")
        return

    st.markdown(f"<h1 style='color: #FF4B4B;'>🛠️ Painel Administrativo - JÁ VENDEU?</h1>", unsafe_allow_html=True)
    st.caption(f"Bem-vindo, Administrador Vitor. Hoje é {datetime.datetime.now().strftime('%d/%m/%Y')}")

    # --- MÉTRICAS RÁPIDAS (ESTATÍSTICAS) ---
    st.markdown("### 📊 Estatísticas da Plataforma")
    col1, col2, col3 = st.columns(3)
    
    try:
        # Busca total de anúncios e usuários para o seu controle
        total_anuncios = len(list(db.collection("anuncios").stream()))
        total_usuarios = len(list(db.collection("usuarios").stream()))
        total_denuncias = len(list(db.collection("denuncias").stream()))
        
        col1.metric("Anúncios Totais", total_anuncios)
        col2.metric("Usuários Cadastrados", total_usuarios)
        col3.metric("Denúncias Pendentes", total_denuncias)
    except:
        st.warning("Erro ao carregar métricas em tempo real.")

    st.markdown("---")

    # --- ABAS DE GERENCIAMENTO ---
    tab_anuncios, tab_denuncias, tab_usuarios = st.tabs(["📢 MODERAR ANÚNCIOS", "🛡️ DENÚNCIAS", "👥 USUÁRIOS"])

    # --- ABA 1: MODERAÇÃO DE ANÚNCIOS (APROVAR, DELETAR, DESTACAR) ---
    with tab_anuncios:
        st.subheader("Gerenciar Vitrine")
        anuncios = db.collection("anuncios").order_by("data_publicacao", direction="DESCENDING").stream()
        
        for doc in anuncios:
            it = doc.to_dict()
            anuncio_id = doc.id
            is_vip = it.get('vip', False) # Verifica se já é destaque
            
            with st.container(border=True):
                c1, c2, c3 = st.columns([1, 3, 2])
                
                with c1:
                    if it.get('fotos'):
                        st.image(f"data:image/jpeg;base64,{it['fotos'][0]}", use_container_width=True)
                
                with c2:
                    st.markdown(f"**{it.get('titulo')}**")
                    st.caption(f"Vendedor: {it.get('vendedor_nome')} ({it.get('vendedor_email')})")
                    st.markdown(f"Preço: R$ {it.get('preco', 0.0):.2f}")
                    if is_vip:
                        st.markdown("⭐ **ESTE ANÚNCIO ESTÁ EM DESTAQUE (VIP)**")
                
                with c3:
                    # Botão para dar o Brinde de Destaque (VIP)
                    if not is_vip:
                        if st.button("⭐ DAR DESTAQUE", key=f"vip_{anuncio_id}", use_container_width=True):
                            db.collection("anuncios").document(anuncio_id).update({"vip": True})
                            st.toast(f"Anúncio de {it.get('vendedor_nome')} agora é VIP!", icon="⭐")
                            st.rerun()
                    else:
                        if st.button("⚪ REMOVER DESTAQUE", key=f"unvip_{anuncio_id}", use_container_width=True):
                            db.collection("anuncios").document(anuncio_id).update({"vip": False})
                            st.rerun()

                    # Botão para Excluir (Moderação agressiva contra lixo/golpe)
                    if st.button("🗑️ EXCLUIR ANÚNCIO", key=f"adm_del_{anuncio_id}", use_container_width=True):
                        db.collection("anuncios").document(anuncio_id).delete()
                        st.success("Anúncio removido!")
                        st.rerun()

    # --- ABA 2: VER DENÚNCIAS REGISTRADAS ---
    with tab_denuncias:
        st.subheader("Alertas de Usuários")
        denuncias = db.collection("denuncias").stream()
        for den in denuncias:
            d = den.to_dict()
            with st.chat_message("user"):
                st.write(f"🚨 **Denúncia no item:** {d.get('titulo')} (ID: {d.get('anuncio_id')})")
                st.write(f"Feita por: {d.get('denunciante')} em {d.get('data')}")
                if st.button("OK, RESOLVIDO", key=f"den_{den.id}"):
                    db.collection("denuncias").document(den.id).delete()
                    st.rerun()

    # --- ABA 3: GERENCIAR USUÁRIOS ---
    with tab_usuarios:
        st.subheader("Lista de Usuários Cadastrados")
        users = db.collection("usuarios").stream()
        for u_doc in users:
            u = u_doc.to_dict()
            st.text(f"👤 {u.get('nome')} | 📧 {u.get('email')} | 📱 {u.get('whatsapp')}")