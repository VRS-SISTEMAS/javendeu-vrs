# =================================================================
# VRS SISTEMAS - JÁ VENDEU?
# MÓDULO: anuncios_vrs.py (GESTÃO SEPARADA: ANUNCIAR VS MEUS ANÚNCIOS)
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
    """Interface que separa a criação de anúncios da gestão de anúncios existentes."""
    if not st.session_state.get('logado'):
        st.warning("⚠️ Faça login primeiro.")
        return

    email_user = st.session_state['usuario']['email']
    pagina_atual = st.session_state.get('pagina_vrs')

    # --- TELA 1: APENAS O FORMULÁRIO DE ANUNCIAR ---
    if pagina_atual == "Anunciar":
        st.markdown("<h1 style='text-align: center;'>➕ Novo Anúncio</h1>", unsafe_allow_html=True)
        with st.container(border=True):
            with st.form("form_vrs_anunciar", clear_on_submit=True):
                t = st.text_input("Título*", placeholder="Ex: Vendo Carro ou Serviço de Guincho")
                desc = st.text_area("Descrição Detalhada*")
                col_p, col_c = st.columns(2)
                p = col_p.number_input("Preço (R$)*", min_value=0.0)
                cat = col_c.selectbox("Categoria*", categorias.obter_categorias_vrs())
                
                st.markdown("📍 Localização")
                col_e, col_ci = st.columns(2)
                est = col_e.selectbox("Estado*", ESTADOS_BR, index=18)
                cid = col_ci.text_input("Cidade*", value="Duque de Caxias")
                f_arq = st.file_uploader("Fotos (Até 3)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

                if st.form_submit_button("🚀 PUBLICAR AGORA"):
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
                        db.collection("anuncios").add(dados)
                        st.success("✅ Anúncio publicado com sucesso!")
                        st.session_state['pagina_vrs'] = "Meus Anúncios" # Redireciona para gestão
                        st.rerun()
                    else:
                        st.error("⚠️ Preencha o título e o preço.")

    # --- TELA 2: APENAS A GESTÃO (MEUS ANÚNCIOS) ---
    elif pagina_atual == "Meus Anúncios":
        st.markdown("<h1 style='text-align: center;'>📂 Meus Anúncios Ativos</h1>", unsafe_allow_html=True)
        
        # Busca apenas os anúncios do usuário logado
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
                    st.write("") # Espaçador
                    if st.button("🗑️ EXCLUIR", key=f"del_{doc.id}", use_container_width=True):
                        db.collection("anuncios").document(doc.id).delete()
                        st.success("Removido!")
                        st.rerun()
        
        if count == 0:
            st.info("Você ainda não tem anúncios ativos. Clique em 'Anunciar' no menu lateral!")