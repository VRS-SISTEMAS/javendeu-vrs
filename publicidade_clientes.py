# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: publicidade_clientes.py (ALCANCE NACIONAL - BRASIL TODO)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime

def gerenciar_banners_vrs(db):
    """Painel administrativo para o Vitor cadastrar publicidade paga."""
    st.subheader("🚀 Gestão de Banners")
    with st.expander("➕ Novo Banner de Cliente"):
        with st.form("f_banner_vrs", clear_on_submit=True):
            cliente = st.text_input("Nome do Cliente")
            link = st.text_input("Link WhatsApp/Site (com https://)")
            # Opção 'Brasil' é a padrão para alcance nacional
            uf = st.selectbox("Estado Alvo", ["Brasil", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])
            arq = st.file_uploader("Upload do Banner (Recomendado: 1200x200px)", type=['png', 'jpg', 'jpeg'])
            
            if st.form_submit_button("ATIVAR PUBLICIDADE"):
                if cliente and link and arq:
                    img = base64.b64encode(arq.getvalue()).decode('utf-8')
                    db.collection("publicidade").add({
                        "cliente": cliente, 
                        "link": link, 
                        "estado_alvo": uf,
                        "foto": img, 
                        "data": datetime.datetime.now()
                    })
                    st.success("Banner ativado com sucesso!")
                    st.rerun()

    # Listagem para remoção
    banners = db.collection("publicidade").order_by("data", direction="DESCENDING").stream()
    for b in banners:
        d = b.to_dict()
        with st.container(border=True):
            st.image(f"data:image/jpeg;base64,{d['foto']}", width=300)
            st.write(f"Cliente: {d['cliente']} | Alvo: {d['estado_alvo']}")
            if st.button("🗑️ Remover Banner", key=f"del_pub_{b.id}"):
                db.collection("publicidade").document(b.id).delete()
                st.rerun()

def exibir_banner_rotativo_vrs(db, estado_atual="Brasil"):
    """
    Exibe o banner na vitrine. 
    LÓGICA NACIONAL: Sempre busca banners marcados como 'Brasil' para aparecer para todos.
    """
    try:
        # Busca banners com alvo 'Brasil' (Independente do filtro do usuário)
        query = db.collection("publicidade").where("estado_alvo", "==", "Brasil").stream()
        lista_banners = [b.to_dict() for b in query]
        
        if lista_banners:
            # Exibe o banner mais recente (o último da lista)
            banner = lista_banners[-1]
            
            # HTML com classe CSS da VRS para ajuste de tela
            st.markdown(f"""
                <div class="vrs-banner-fix" style="width:100%; margin-top: 10px; margin-bottom: 30px;">
                    <a href="{banner['link']}" target="_blank">
                        <img src="data:image/jpeg;base64,{banner['foto']}" 
                             style="width:100%; border-radius:10px; border: 1px solid #333; box-shadow: 0px 4px 15px rgba(0,0,0,0.5);">
                    </a>
                </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        # Falha silenciosa para não quebrar a vitrine com o erro vermelho
        pass