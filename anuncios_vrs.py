# =================================================================
# VRS Soluções
# JÁ VENDEU? - GESTÃO DE ANÚNCIOS (CENTRALIZAÇÃO TOTAL)
# MÓDULO: anuncios_vrs.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime
import categorias

def exibir_painel_vendedor(db):
    """Interface para gerenciar anúncios do usuário logado."""
    if not st.session_state.get('logado'):
        st.warning("⚠️ Você precisa estar logado para acessar seus anúncios.")
        return

    email_user = st.session_state['usuario']['email']

    # Estilização CSS para o painel
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
        with st.expander("📝 Detalhes do Produto", expanded=True):
            with st.form("form_final_vrs"):
                t = st.text_input("Título do Anúncio*")
                desc = st.text_area("Descrição (Conte detalhes do produto)")
                cp, cc = st.columns(2)
                p = cp.number_input("Preço (R$)*", min_value=0.0, step=0.01)
                cat = cc.selectbox("Categoria*", categorias.obter_categorias_vrs())
                f = st.file_uploader("Foto do Produto*", type=['png', 'jpg', 'jpeg'])
                
                if st.form_submit_button("🚀 PUBLICAR AGORA"):
                    if t and p > 0 and f:
                        foto_b64 = base64.b64encode(f.getvalue()).decode('utf-8')
                        db.collection("anuncios").add({
                            "titulo": t, 
                            "descricao": desc,
                            "preco": p, 
                            "categoria": cat, 
                            "foto": foto_b64,
                            "status": "ativo", 
                            "vendedor_email": email_user,
                            "vendedor_nome": st.session_state['usuario']['nome'],
                            "data_publicacao": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                        })
                        st.success("Anúncio publicado com sucesso!")
                        st.session_state['vrs_novo_post'] = False
                        st.rerun()
                    else:
                        st.error("Por favor, preencha Título, Preço e anexe uma Foto.")
            
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
                    if 'foto' in item:
                        st.image(f"data:image/jpeg;base64,{item['foto']}", use_container_width=True)
                with ct:
                    st.subheader(item['titulo'])
                    st.write(f"**R$ {item['preco']:.2f}**")
                    st.caption(f"Publicado em: {item.get('data_publicacao', 'N/A')}")
                with cb:
                    if st.button("🗑️", key=f"del_{doc.id}"):
                        db.collection("anuncios").document(doc.id).delete()
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            
            if count == 0:
                st.info(f"Nenhum anúncio com status '{status.upper()}' encontrado.")