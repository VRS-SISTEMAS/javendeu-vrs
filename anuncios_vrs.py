# =================================================================
# VRS SISTEMAS
# JÁ VENDEU? - GESTÃO DE ANÚNCIOS (EDIÇÃO E SUPORTE A 3 FOTOS)
# MÓDULO: anuncios_vrs.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime
import categorias

def exibir_painel_vendedor(db):
    """Interface para gerenciar anúncios do usuário logado com múltiplas fotos e edição."""
    if not st.session_state.get('logado'):
        st.warning("⚠️ Você precisa estar logado para acessar seus anúncios.")
        return

    email_user = st.session_state['usuario']['email']

    # Estilização CSS para o painel de anúncios
    st.markdown("""
        <style>
        .main .block-container { max-width: 1000px !important; margin: 0 auto !important; }
        .card-vrs-final {
            background-color: #1A1C24;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #333;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>📂 Gestão de Anúncios</h1>", unsafe_allow_html=True)

    # Botão para Novo Anúncio
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("➕ NOVO ANÚNCIO", use_container_width=True, type="primary"):
            st.session_state['vrs_novo_post'] = True
            st.session_state['vrs_editando_id'] = None # Garante que não está editando

    # --- LÓGICA DE CRIAÇÃO / EDIÇÃO ---
    if st.session_state.get('vrs_novo_post') or st.session_state.get('vrs_editando_id'):
        modo_edicao = st.session_state.get('vrs_editando_id') is not None
        titulo_painel = "📝 Editar Anúncio" if modo_edicao else "📝 Detalhes do Novo Produto"
        
        # Se for edição, busca os dados atuais
        dados_atuais = {}
        if modo_edicao:
            doc_ref = db.collection("anuncios").document(st.session_state['vrs_editando_id']).get()
            if doc_ref.exists:
                dados_atuais = doc_ref.to_dict()

        with st.expander(titulo_painel, expanded=True):
            with st.form("form_vrs_anuncio"):
                t = st.text_input("Título do Anúncio*", value=dados_atuais.get('titulo', ""))
                desc = st.text_area("Descrição (Conte detalhes do produto)", value=dados_atuais.get('descricao', ""))
                cp, cc = st.columns(2)
                p = cp.number_input("Preço (R$)*", min_value=0.0, step=0.01, value=float(dados_atuais.get('preco', 0.0)))
                
                # Categoria com index automático na edição
                lista_cats = categorias.obter_categorias_vrs()
                idx_cat = lista_cats.index(dados_atuais['categoria']) if modo_edicao and dados_atuais.get('categoria') in lista_cats else 0
                cat = cc.selectbox("Categoria*", lista_cats, index=idx_cat)
                
                f_arquivos = st.file_uploader("Fotos (Selecione até 3)*", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
                st.caption("⚠️ Se editar e não enviar fotos novas, manteremos as fotos atuais.")

                if st.form_submit_button("🚀 SALVAR E PUBLICAR"):
                    if t and p > 0:
                        # Processamento de fotos
                        if f_arquivos:
                            if len(f_arquivos) > 3:
                                st.error("❌ Máximo de 3 fotos permitido.")
                            else:
                                lista_fotos_b64 = []
                                for arq in f_arquivos:
                                    b64 = base64.b64encode(arq.getvalue()).decode('utf-8')
                                    lista_fotos_b64.append(b64)
                                dados_post = {
                                    "titulo": t, "descricao": desc, "preco": p, "categoria": cat,
                                    "fotos": lista_fotos_b64, "status": "ativo", "vendedor_email": email_user,
                                    "vendedor_nome": st.session_state['usuario']['nome'],
                                    "data_publicacao": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                                }
                        else:
                            # Se está editando e não mandou fotos novas, mantém as velhas
                            if modo_edicao:
                                dados_post = {
                                    "titulo": t, "descricao": desc, "preco": p, "categoria": cat
                                }
                            else:
                                st.error("⚠️ Envie ao menos 1 foto para novos anúncios.")
                                st.stop()

                        # Salva no Firebase (Update ou Add)
                        if modo_edicao:
                            db.collection("anuncios").document(st.session_state['vrs_editando_id']).update(dados_post)
                            st.success("✅ Anúncio atualizado com sucesso!")
                        else:
                            db.collection("anuncios").add(dados_post)
                            st.success("✅ Anúncio publicado!")
                        
                        st.session_state['vrs_novo_post'] = False
                        st.session_state['vrs_editando_id'] = None
                        st.rerun()
                    else:
                        st.error("⚠️ Título e Preço são obrigatórios.")

            if st.button("Cancelar"):
                st.session_state['vrs_novo_post'] = False
                st.session_state['vrs_editando_id'] = None
                st.rerun()

    st.markdown("---")
    tabs = st.tabs(["✅ ATIVOS", "💰 VENDIDOS", "⏳ PENDENTES", "🚫 INATIVOS"])
    status_list = ["ativo", "vendido", "pendente", "inativo"]

    for i, status in enumerate(status_list):
        with tabs[i]:
            itens = db.collection("anuncios").where("vendedor_email", "==", email_user).where("status", "==", status).stream()
            count = 0
            for doc in itens:
                count += 1
                item = doc.to_dict()
                st.markdown("<div class='card-vrs-final'>", unsafe_allow_html=True)
                ci, ct, cb = st.columns([1, 3, 1.2])
                
                with ci: 
                    if 'fotos' in item and item['fotos']:
                        st.image(f"data:image/jpeg;base64,{item['fotos'][0]}", use_container_width=True)
                    elif 'foto' in item:
                        st.image(f"data:image/jpeg;base64,{item['foto']}", use_container_width=True)
                
                with ct:
                    st.subheader(item.get('titulo', 'Sem Título'))
                    st.write(f"**R$ {item.get('preco', 0):.2f}**")
                    st.caption(f"Publicado em: {item.get('data_publicacao', 'N/A')}")
                
                with cb:
                    # BOTÕES DE AÇÃO: EDITAR E DELETAR
                    col_edit, col_del = st.columns(2)
                    with col_edit:
                        if st.button("📝", key=f"edit_{doc.id}", help="Editar anúncio"):
                            st.session_state['vrs_editando_id'] = doc.id
                            st.session_state['vrs_novo_post'] = False
                            st.rerun()
                    with col_del:
                        if st.button("🗑️", key=f"del_{doc.id}", help="Excluir anúncio"):
                            db.collection("anuncios").document(doc.id).delete()
                            st.rerun()
                            
                    # BOTÃO PARA MUDAR STATUS (Ex: Marcar como vendido se estiver ativo)
                    if status == "ativo":
                        if st.button("Marcar Vendido", key=f"sell_{doc.id}", use_container_width=True):
                            db.collection("anuncios").document(doc.id).update({"status": "vendido"})
                            st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)
            
            if count == 0:
                st.info(f"Nenhum anúncio encontrado em {status.upper()}.")