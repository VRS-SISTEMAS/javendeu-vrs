# =================================================================
# VRS SISTEMAS
# JÁ VENDEU? - GESTÃO DE ANÚNCIOS (SUPORTE A 3 FOTOS)
# MÓDULO: anuncios_vrs.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime
import categorias

def exibir_painel_vendedor(db):
    """Interface para gerenciar anúncios do usuário logado com múltiplas fotos."""
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

    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("➕ NOVO ANÚNCIO", use_container_width=True, type="primary"):
            st.session_state['vrs_novo_post'] = True

    if st.session_state.get('vrs_novo_post'):
        with st.expander("📝 Detalhes do Produto (Máximo 3 Fotos)", expanded=True):
            with st.form("form_final_vrs"):
                t = st.text_input("Título do Anúncio*")
                desc = st.text_area("Descrição (Conte detalhes do produto)")
                cp, cc = st.columns(2)
                p = cp.number_input("Preço (R$)*", min_value=0.0, step=0.01)
                cat = cc.selectbox("Categoria*", categorias.obter_categorias_vrs())
                
                # NOVIDADE: Aceita até 3 fotos simultâneas
                f_arquivos = st.file_uploader("Fotos do Produto (Selecione até 3)*", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
                
                if st.form_submit_button("🚀 PUBLICAR AGORA"):
                    if t and p > 0 and f_arquivos:
                        if len(f_arquivos) > 3:
                            st.error("❌ Por favor, selecione no máximo 3 fotos.")
                        else:
                            # Converte todas as fotos selecionadas para Base64
                            lista_fotos_b64 = []
                            for arq in f_arquivos:
                                b64 = base64.b64encode(arq.getvalue()).decode('utf-8')
                                lista_fotos_b64.append(b64)
                            
                            # Salva no Firebase com o campo 'fotos' (lista)
                            db.collection("anuncios").add({
                                "titulo": t, 
                                "descricao": desc,
                                "preco": p, 
                                "categoria": cat, 
                                "fotos": lista_fotos_b64, # LISTA DE FOTOS
                                "status": "ativo", 
                                "vendedor_email": email_user,
                                "vendedor_nome": st.session_state['usuario']['nome'],
                                "data_publicacao": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                            })
                            st.success("✅ Anúncio publicado com 3 fotos!")
                            st.session_state['vrs_novo_post'] = False
                            st.rerun()
                    else:
                        st.error("⚠️ Preencha os campos obrigatórios e envie ao menos 1 foto.")
            
            if st.button("Cancelar"):
                st.session_state['vrs_novo_post'] = False
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
                ci, ct, cb = st.columns([1, 3, 1])
                with ci: 
                    # Mostra apenas a primeira foto na gestão
                    if 'fotos' in item and item['fotos']:
                        st.image(f"data:image/jpeg;base64,{item['fotos'][0]}", use_container_width=True)
                    elif 'foto' in item: # Compatibilidade com anúncios antigos
                        st.image(f"data:image/jpeg;base64,{item['foto']}", use_container_width=True)
                with ct:
                    st.subheader(item.get('titulo', 'Sem Título'))
                    st.write(f"**R$ {item.get('preco', 0):.2f}**")
                    st.caption(f"Publicado em: {item.get('data_publicacao', 'N/A')}")
                with cb:
                    if st.button("🗑️", key=f"del_{doc.id}"):
                        db.collection("anuncios").document(doc.id).delete()
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            
            if count == 0:
                st.info(f"Nenhum anúncio encontrado.")