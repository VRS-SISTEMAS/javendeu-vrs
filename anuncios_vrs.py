# =================================================================
# VRS SISTEMAS - JÁ VENDEU?
# MÓDULO: anuncios_vrs.py (VERSÃO BLINDADA ANTI-GOLPE)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime
import categorias

ESTADOS_BR = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

def exibir_alerta_seguranca_vrs():
    """Exibe o banner visual de trava anti-golpe nos anúncios."""
    st.markdown("""
        <div style='background-color: #4B0000; padding: 15px; border: 2px solid #FF4B4B; border-radius: 10px; margin-bottom: 20px;'>
            <h4 style='color: white; margin: 0;'>🛡️ SEGURANÇA VRS SOLUÇÕES</h4>
            <p style='color: #FFCBCB; font-size: 14px; margin: 5px 0 0 0;'>
                <b>CUIDADO:</b> Nunca faça depósitos antecipados. Negocie pessoalmente em locais públicos e verifique o produto antes de pagar.
            </p>
        </div>
    """, unsafe_allow_html=True)

def registrar_denuncia_vrs(db, anuncio_id, anuncio_titulo):
    """Registra uma denúncia no banco de dados para análise do Vitor."""
    if db:
        db.collection("denuncias").add({
            "anuncio_id": anuncio_id,
            "titulo": anuncio_titulo,
            "data": datetime.datetime.now(),
            "denunciante": st.session_state['usuario']['email'] if st.session_state.get('logado') else "Anônimo"
        })
        st.toast("Denúncia enviada. A VRS Soluções irá analisar!", icon="🛡️")

def exibir_painel_vendedor(db):
    """Interface para gerenciar anúncios com as novas travas e categorias."""
    if not st.session_state.get('logado'):
        st.warning("⚠️ Você precisa estar logado para acessar seus anúncios.")
        return

    email_user = st.session_state['usuario']['email']

    st.markdown("<h1 style='text-align: center;'>📂 Gestão de Anúncios VRS</h1>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("➕ NOVO ANÚNCIO", use_container_width=True, type="primary"):
            st.session_state['vrs_novo_post'] = True
            st.session_state['vrs_editando_id'] = None 

    if st.session_state.get('vrs_novo_post') or st.session_state.get('vrs_editando_id'):
        modo_edicao = st.session_state.get('vrs_editando_id') is not None
        titulo_painel = "📝 Editar Anúncio" if modo_edicao else "📝 Detalhes do Novo Produto/Serviço"
        
        dados_atuais = {}
        if modo_edicao:
            doc_ref = db.collection("anuncios").document(st.session_state['vrs_editando_id']).get()
            if doc_ref.exists:
                dados_atuais = doc_ref.to_dict()

        with st.expander(titulo_painel, expanded=True):
            with st.form("form_vrs_anuncio"):
                t = st.text_input("Título do Anúncio*", value=dados_atuais.get('titulo', ""), placeholder="Ex: Vendo Carro ou Serviço de Guincho")
                desc = st.text_area("Descrição Detalhada*", value=dados_atuais.get('descricao', ""))
                
                col_p, col_c = st.columns(2)
                p = col_p.number_input("Preço (R$)*", min_value=0.0, step=0.01, value=float(dados_atuais.get('preco', 0.0)))
                
                lista_cats = categorias.obter_categorias_vrs()
                idx_cat = lista_cats.index(dados_atuais['categoria']) if modo_edicao and dados_atuais.get('categoria') in lista_cats else 0
                cat = col_c.selectbox("Categoria*", lista_cats, index=idx_cat)

                st.markdown("📍 **Localização**")
                col_est, col_cid = st.columns(2)
                idx_est = ESTADOS_BR.index(dados_atuais['estado']) if modo_edicao and dados_atuais.get('estado') in ESTADOS_BR else 18 
                est = col_est.selectbox("Estado*", ESTADOS_BR, index=idx_est)
                cid = col_cid.text_input("Cidade*", value=dados_atuais.get('cidade', "Duque de Caxias"))
                
                f_arquivos = st.file_uploader("Fotos (Selecione até 3)*", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

                if st.form_submit_button("🚀 PUBLICAR NO JÁ VENDEU?"):
                    if t and p > 0 and cid:
                        lista_fotos_b64 = []
                        if f_arquivos:
                            for arq in f_arquivos[:3]:
                                b64 = base64.b64encode(arq.getvalue()).decode('utf-8')
                                lista_fotos_b64.append(b64)
                        
                        dados_post = {
                            "titulo": t, "descricao": desc, "preco": p, "categoria": cat,
                            "estado": est, "cidade": cid.strip().title(),
                            "status": "ativo", "vendedor_email": email_user,
                            "vendedor_nome": st.session_state['usuario']['nome'],
                            "vendedor_whatsapp": st.session_state['usuario'].get('whatsapp', ''),
                            "data_publicacao": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                        }
                        if lista_fotos_b64: dados_post["fotos"] = lista_fotos_b64

                        if modo_edicao:
                            db.collection("anuncios").document(st.session_state['vrs_editando_id']).update(dados_post)
                        else:
                            db.collection("anuncios").add(dados_post)
                        
                        st.success("✅ Sucesso!")
                        st.session_state['vrs_novo_post'] = False
                        st.session_state['vrs_editando_id'] = None
                        st.rerun()
                    else:
                        st.error("⚠️ Preencha os campos obrigatórios.")

    # Listagem de anúncios simplificada para o Vendedor
    tabs = st.tabs(["✅ ATIVOS", "💰 VENDIDOS", "🚫 INATIVOS"])
    status_list = ["ativo", "vendido", "inativo"]
    for i, status in enumerate(status_list):
        with tabs[i]:
            itens = db.collection("anuncios").where("vendedor_email", "==", email_user).where("status", "==", status).stream()
            for doc in itens:
                item = doc.to_dict()
                with st.container(border=True):
                    c_img, c_txt, c_btn = st.columns([1, 3, 1])
                    with c_img:
                        if item.get('fotos'): st.image(f"data:image/jpeg;base64,{item['fotos'][0]}", use_container_width=True)
                    with c_txt:
                        st.write(f"**{item['titulo']}**")
                        st.caption(f"R$ {item['preco']:.2f}")
                    with c_btn:
                        if st.button("🗑️", key=f"del_{doc.id}"):
                            db.collection("anuncios").document(doc.id).delete()
                            st.rerun()