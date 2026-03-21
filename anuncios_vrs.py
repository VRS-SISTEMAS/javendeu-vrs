# =================================================================
# VRS SISTEMAS - JÁ VENDEU?
# MÓDULO: anuncios_vrs.py (VERSÃO GESTÃO COMPLETA: ANUNCIAR, EXCLUIR E EDITAR)
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
    """Interface que separa a criação/edição da gestão de anúncios existentes."""
    if not st.session_state.get('logado'):
        st.warning("⚠️ Faça login primeiro.")
        return

    email_user = st.session_state['usuario']['email']
    pagina_atual = st.session_state.get('pagina_vrs')

    # --- LÓGICA DE CADASTRO OU EDIÇÃO (TELA DE FORMULÁRIO) ---
    # Entra aqui se estiver em 'Anunciar' ou se houver um ID para editar
    id_para_editar = st.session_state.get('vrs_editando_id')
    
    if pagina_atual == "Anunciar" or id_para_editar:
        titulo_acao = "📝 Editar Anúncio" if id_para_editar else "➕ Novo Anúncio"
        st.markdown(f"<h1 style='text-align: center;'>{titulo_acao}</h1>", unsafe_allow_html=True)
        
        # Se for edição, busca os dados atuais no banco
        dados_atuais = {}
        if id_para_editar:
            doc_ref = db.collection("anuncios").document(id_para_editar).get()
            if doc_ref.exists:
                dados_atuais = doc_ref.to_dict()

        with st.container(border=True):
            with st.form("form_vrs_anunciar", clear_on_submit=True):
                t = st.text_input("Título*", value=dados_atuais.get('titulo', ""), placeholder="Ex: Vendo Carro")
                desc = st.text_area("Descrição Detalhada*", value=dados_atuais.get('descricao', ""))
                col_p, col_c = st.columns(2)
                p = col_p.number_input("Preço (R$)*", min_value=0.0, value=float(dados_atuais.get('preco', 0.0)))
                
                # Categoria (busca index correto)
                lista_cats = categorias.obter_categorias_vrs()
                idx_cat = lista_cats.index(dados_atuais['categoria']) if id_para_editar and dados_atuais.get('categoria') in lista_cats else 0
                cat = col_c.selectbox("Categoria*", lista_cats, index=idx_cat)
                
                st.markdown("📍 Localização")
                col_e, col_ci = st.columns(2)
                # Estado (busca index)
                idx_est = ESTADOS_BR.index(dados_atuais['estado']) if id_para_editar and dados_atuais.get('estado') in ESTADOS_BR else 18
                est = col_e.selectbox("Estado*", ESTADOS_BR, index=idx_est)
                cid = col_ci.text_input("Cidade*", value=dados_atuais.get('cidade', "Duque de Caxias"))
                
                st.caption("📷 Se quiser mudar as fotos, selecione novas abaixo (máximo 3).")
                f_arq = st.file_uploader("Fotos", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

                c_env, c_can = st.columns(2)
                btn_texto = "💾 SALVAR ALTERAÇÕES" if id_para_editar else "🚀 PUBLICAR AGORA"
                
                if c_env.form_submit_button(btn_texto, use_container_width=True):
                    if t and p > 0:
                        # Prepara dados
                        dados = {
                            "titulo": t, "descricao": desc, "preco": p, "categoria": cat,
                            "estado": est, "cidade": cid.strip().title(), "status": "ativo",
                            "vendedor_email": email_user,
                            "vendedor_nome": st.session_state['usuario']['nome'],
                            "vendedor_whatsapp": st.session_state['usuario'].get('whatsapp', ''),
                            "data_publicacao": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                        }
                        
                        # Processa fotos novas se houver
                        if f_arq:
                            lista_f = [base64.b64encode(a.getvalue()).decode('utf-8') for a in f_arq[:3]]
                            dados["fotos"] = lista_f
                        
                        # Executa ação no Firebase
                        if id_para_editar:
                            db.collection("anuncios").document(id_para_editar).update(dados)
                            st.success("✅ Anúncio atualizado!")
                            st.session_state['vrs_editando_id'] = None # Limpa trava de edição
                        else:
                            db.collection("anuncios").add(dados)
                            st.success("✅ Anúncio publicado!")
                        
                        st.session_state['pagina_vrs'] = "Meus Anúncios"
                        st.rerun()

                if c_can.form_submit_button("❌ CANCELAR", use_container_width=True):
                    st.session_state['vrs_editando_id'] = None
                    st.session_state['pagina_vrs'] = "Meus Anúncios"
                    st.rerun()

    # --- TELA 2: GESTÃO (MEUS ANÚNCIOS) COM BOTÃO EDITAR ---
    elif pagina_atual == "Meus Anúncios":
        st.markdown("<h1 style='text-align: center;'>📂 Meus Anúncios Ativos</h1>", unsafe_allow_html=True)
        
        itens = db.collection("anuncios").where("vendedor_email", "==", email_user).stream()
        count = 0
        for doc in itens:
            count += 1
            it = doc.to_dict()
            with st.container(border=True):
                ci, ct, cb = st.columns([1, 3, 1.2]) 
                with ci:
                    if it.get('fotos'): 
                        st.image(f"data:image/jpeg;base64,{it['fotos'][0]}", use_container_width=True)
                with ct:
                    st.subheader(it.get('titulo', 'Sem Título'))
                    st.markdown(f"<h3 style='color: #FF4B4B; margin:0;'>R$ {it.get('preco', 0):.2f}</h3>", unsafe_allow_html=True)
                    st.caption(f"📍 {it.get('cidade')} - {it.get('estado')} | STATUS: {it.get('status').upper()}")
                with cb:
                    # Botão Editar
                    if st.button("📝 EDITAR", key=f"edit_{doc.id}", use_container_width=True):
                        st.session_state['vrs_editando_id'] = doc.id
                        st.rerun()
                    
                    # Botão Excluir
                    if st.button("🗑️ EXCLUIR", key=f"del_{doc.id}", use_container_width=True):
                        db.collection("anuncios").document(doc.id).delete()
                        st.rerun()
        
        if count == 0:
            st.info("Você ainda não tem anúncios ativos.")