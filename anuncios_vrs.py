# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: anuncios_vrs.py (GESTÃO DE ANÚNCIOS - EDIÇÃO RESTAURADA)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime
import categorias

ESTADOS_BR = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

def exibir_painel_vendedor(db):
    """Interface completa da VRS para criar e gerenciar anúncios."""
    if not st.session_state.get('logado'):
        st.warning("⚠️ Por favor, acesse sua conta primeiro.")
        return

    email_user = st.session_state['usuario']['email']
    pagina_atual = st.session_state.get('pagina_vrs')
    id_para_editar = st.session_state.get('vrs_editando_id')
    
    # --- FLUXO DE CRIAÇÃO OU EDIÇÃO ---
    if pagina_atual == "Anunciar" or id_para_editar:
        st.subheader("📝 Editar Anúncio" if id_para_editar else "➕ Novo Anúncio")
        dados_atuais = {}
        if id_para_editar:
            doc = db.collection("anuncios").document(id_para_editar).get()
            if doc.exists: dados_atuais = doc.to_dict()

        with st.form("form_vrs_anunciar", clear_on_submit=True):
            t = st.text_input("Título*", value=dados_atuais.get('titulo', ""), placeholder="Ex: Notebook Gamer")
            desc = st.text_area("Descrição*", value=dados_atuais.get('descricao', ""), height=150)
            
            c1, c2 = st.columns(2)
            p = c1.number_input("Preço (R$)*", min_value=0.0, value=float(dados_atuais.get('preco', 0.0)))
            cat_list = categorias.obter_categorias_vrs()
            cat = c2.selectbox("Categoria*", cat_list, index=cat_list.index(dados_atuais.get('categoria')) if dados_atuais.get('categoria') in cat_list else 0)
            
            st.markdown("📍 Localização")
            loc1, loc2 = st.columns(2)
            est = loc1.selectbox("Estado*", ESTADOS_BR, index=ESTADOS_BR.index(dados_atuais.get('estado')) if dados_atuais.get('estado') in ESTADOS_BR else 18)
            cid = loc2.text_input("Cidade*", value=dados_atuais.get('cidade', ""))
            
            f_arq = st.file_uploader("Fotos (Máx 3)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

            btn_label = "💾 SALVAR ALTERAÇÕES" if id_para_editar else "🚀 PUBLICAR"
            if st.form_submit_button(btn_label, use_container_width=True):
                if t and cid and p > 0:
                    dados = {
                        "titulo": t, "descricao": desc, "preco": p, "categoria": cat,
                        "estado": est, "cidade": cid.strip().title(), "status": "ativo",
                        "vendedor_email": email_user,
                        "vendedor_nome": st.session_state['usuario']['nome'],
                        "data_publicacao": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    }
                    if f_arq:
                        dados["fotos"] = [base64.b64encode(a.getvalue()).decode('utf-8') for a in f_arq[:3]]
                    
                    if id_para_editar:
                        db.collection("anuncios").document(id_para_editar).update(dados)
                        st.success("✅ Alterações salvas!")
                    else:
                        db.collection("anuncios").add(dados)
                        st.success("✅ Anúncio publicado!")
                    
                    st.session_state['vrs_editando_id'] = None
                    st.session_state['pagina_vrs'] = "Meus Anúncios"
                    st.rerun()

    # --- LISTAGEM DE MEUS ANÚNCIOS (BOTAO EDITAR VOLTOU!) ---
    elif pagina_atual == "Meus Anúncios":
        st.subheader("📂 Gerenciar Meus Anúncios")
        itens = db.collection("anuncios").where("vendedor_email", "==", email_user).stream()
        
        count = 0
        for doc in itens:
            count += 1
            it = doc.to_dict()
            with st.container(border=True):
                col_i, col_t, col_b = st.columns([1, 2.5, 1.2])
                with col_i:
                    f_list = it.get('fotos', [])
                    if f_list: st.image(f"data:image/jpeg;base64,{f_list[0]}", use_container_width=True)
                with col_t:
                    st.markdown(f"**{it.get('titulo')}**")
                    st.markdown(f"<h4 style='color: #FF4B4B;'>R$ {it.get('preco'):.2f}</h4>", unsafe_allow_html=True)
                    st.caption(f"📍 {it.get('cidade')} - {it.get('estado')}")
                with col_b:
                    # BOTAO EDITAR RESTAURADO
                    if st.button("📝 EDITAR", key=f"btn_edit_{doc.id}", use_container_width=True):
                        st.session_state['vrs_editando_id'] = doc.id
                        st.rerun()
                    
                    if st.button("🗑️ EXCLUIR", key=f"btn_del_{doc.id}", use_container_width=True):
                        db.collection("anuncios").document(doc.id).delete()
                        st.rerun()
        
        if count == 0:
            st.info("Você ainda não tem anúncios ativos.")