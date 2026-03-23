# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: anuncios_vrs.py (VERSÃO RESTAURADA E COMPLETA)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime
import categorias

ESTADOS_BR = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

def exibir_painel_vendedor(db):
    """Interface para gerenciar anúncios do usuário logado na VRS."""
    if not st.session_state.get('logado'):
        st.warning("⚠️ Faça login primeiro.")
        return

    email_user = st.session_state['usuario']['email']
    pagina_atual = st.session_state.get('pagina_vrs')
    id_para_editar = st.session_state.get('vrs_editando_id')
    
    if pagina_atual == "Anunciar" or id_para_editar:
        st.subheader("➕ Publicar Anúncio" if not id_para_editar else "📝 Editar Anúncio")
        dados_atuais = {}
        if id_para_editar:
            doc = db.collection("anuncios").document(id_para_editar).get()
            if doc.exists: dados_atuais = doc.to_dict()

        with st.form("form_vrs_anunciar", clear_on_submit=True):
            t = st.text_input("Título*", value=dados_atuais.get('titulo', ""))
            desc = st.text_area("Descrição*", value=dados_atuais.get('descricao', ""))
            p = st.number_input("Preço (R$)*", min_value=0.0, value=float(dados_atuais.get('preco', 0.0)))
            
            col_loc1, col_loc2 = st.columns(2)
            est = col_loc1.selectbox("Estado*", ESTADOS_BR, index=ESTADOS_BR.index(dados_atuais.get('estado', "RJ")) if dados_atuais.get('estado') in ESTADOS_BR else 18)
            cid = col_loc2.text_input("Cidade*", value=dados_atuais.get('cidade', ""))
            
            cat = st.selectbox("Categoria*", categorias.obter_categorias_vrs())
            f_arq = st.file_uploader("Fotos (Até 3)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

            if st.form_submit_button("SALVAR ANÚNCIO", use_container_width=True):
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
                    else:
                        db.collection("anuncios").add(dados)
                    
                    st.success("✅ Sucesso na VRS Soluções!")
                    st.session_state['vrs_editando_id'] = None
                    st.session_state['pagina_vrs'] = "Meus Anúncios"
                    st.rerun()

    elif pagina_atual == "Meus Anúncios":
        st.subheader("📂 Meus Anúncios")
        itens = db.collection("anuncios").where("vendedor_email", "==", email_user).stream()
        for doc in itens:
            it = doc.to_dict()
            with st.container(border=True):
                col_i, col_t, col_b = st.columns([1, 2, 1])
                with col_i:
                    if it.get('fotos'): st.image(f"data:image/jpeg;base64,{it['fotos'][0]}", use_container_width=True)
                with col_t:
                    st.write(f"**{it.get('titulo')}**")
                    st.write(f"R$ {it.get('preco'):.2f}")
                    st.caption(f"📍 {it.get('cidade')} - {it.get('estado')}")
                with col_b:
                    if st.button("🗑️", key=f"del_{doc.id}"):
                        db.collection("anuncios").document(doc.id).delete()
                        st.rerun()