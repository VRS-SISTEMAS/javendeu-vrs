# =================================================================
# VRS SISTEMAS - JÁ VENDEU?
# MÓDULO: anuncios_vrs.py (VERSÃO CORRIGIDA - VISUAL ORIGINAL)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime
import categorias

ESTADOS_BR = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

def exibir_alerta_seguranca_vrs():
    """Exibe o banner visual de trava anti-golpe."""
    st.markdown("""
        <div style='background-color: #4B0000; padding: 15px; border: 2px solid #FF4B4B; border-radius: 10px; margin-bottom: 20px;'>
            <h4 style='color: white; margin: 0;'>🛡️ SEGURANÇA VRS SOLUÇÕES</h4>
            <p style='color: #FFCBCB; font-size: 14px; margin: 5px 0 0 0;'>
                <b>CUIDADO:</b> Nunca faça depósitos antecipados. Negocie pessoalmente em locais públicos!
            </p>
        </div>
    """, unsafe_allow_html=True)

def registrar_denuncia_vrs(db, anuncio_id, anuncio_titulo):
    """Registra uma denúncia para análise do Vitor."""
    if db:
        db.collection("denuncias").add({
            "anuncio_id": anuncio_id, "titulo": anuncio_titulo,
            "data": datetime.datetime.now(),
            "denunciante": st.session_state['usuario']['email'] if st.session_state.get('logado') else "Anônimo"
        })
        st.toast("Denúncia enviada à VRS Soluções!", icon="🛡️")

def exibir_painel_vendedor(db):
    """Interface de gestão com o visual original VRS."""
    if not st.session_state.get('logado'):
        st.warning("⚠️ Faça login primeiro.")
        return

    email_user = st.session_state['usuario']['email']
    st.markdown("<h1 style='text-align: center;'>📂 Gestão de Anúncios VRS</h1>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("➕ NOVO ANÚNCIO", use_container_width=True, type="primary"):
            st.session_state['vrs_novo_post'] = True
            st.session_state['vrs_editando_id'] = None 

    # LÓGICA DE CADASTRO/EDIÇÃO (MANTIDA)
    if st.session_state.get('vrs_novo_post') or st.session_state.get('vrs_editando_id'):
        modo_e = st.session_state.get('vrs_editando_id') is not None
        with st.form("form_vrs_anuncio"):
            t = st.text_input("Título*", placeholder="Ex: Vendo Carro")
            desc = st.text_area("Descrição*")
            col_p, col_c = st.columns(2)
            p = col_p.number_input("Preço (R$)*", min_value=0.0)
            cat = col_c.selectbox("Categoria*", categorias.obter_categorias_vrs())
            
            st.markdown("📍 Localização")
            col_e, col_ci = st.columns(2)
            est = col_e.selectbox("Estado*", ESTADOS_BR, index=18)
            cid = col_ci.text_input("Cidade*", value="Duque de Caxias")
            f_arq = st.file_uploader("Fotos (Até 3)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

            if st.form_submit_button("🚀 PUBLICAR"):
                if t and p > 0:
                    lista_f = [base64.b64encode(a.getvalue()).decode('utf-8') for a in f_arq[:3]]
                    dados = {
                        "titulo": t, "descricao": desc, "preco": p, "categoria": cat,
                        "estado": est, "cidade": cid.strip().title(), "status": "ativo",
                        "vendedor_email": email_user,
                        "vendedor_nome": st.session_state['usuario']['nome'],
                        "vendedor_whatsapp": st.session_state['usuario'].get('whatsapp', ''),
                        "data_publicacao": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    }
                    if lista_f: dados["fotos"] = lista_f
                    if modo_e: db.collection("anuncios").document(st.session_state['vrs_editando_id']).update(dados)
                    else: db.collection("anuncios").add(dados)
                    st.success("✅ Sucesso!")
                    st.session_state['vrs_novo_post'] = False
                    st.rerun()

    st.markdown("---")
    # VOLTANDO AO VISUAL DE CARDS COM COLUNAS NA GESTÃO
    itens = db.collection("anuncios").where("vendedor_email", "==", email_user).stream()
    for doc in itens:
        it = doc.to_dict()
        with st.container(border=True):
            ci, ct, cb = st.columns([1, 3, 1.2]) # Estrutura original de 3 colunas por card
            with ci:
                if it.get('fotos'): st.image(f"data:image/jpeg;base64,{it['fotos'][0]}", use_container_width=True)
            with ct:
                st.subheader(it.get('titulo', 'Sem Título'))
                st.write(f"**R$ {it.get('preco', 0):.2f}**")
                st.caption(f"📍 {it.get('cidade')} - {it.get('estado')} | {it.get('status').upper()}")
            with cb:
                if st.button("🗑️ EXCLUIR", key=f"del_{doc.id}", use_container_width=True):
                    db.collection("anuncios").document(doc.id).delete()
                    st.rerun()