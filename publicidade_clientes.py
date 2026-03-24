# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: publicidade_clientes.py (CORREÇÃO DE GRAVAÇÃO E EXIBIÇÃO)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime

def gerenciar_banners_vrs(db):
    """Painel para o Vitor cadastrar publicidade paga."""
    st.subheader("🚀 Gestão de Banners")
    
    # Formulário para novo banner
    with st.expander("➕ Novo Banner de Cliente", expanded=True):
        with st.form("f_banner_vrs", clear_on_submit=True):
            cliente = st.text_input("Nome do Cliente")
            link = st.text_input("Link WhatsApp/Site (com https://)")
            uf = st.selectbox("Estado Alvo", ["Brasil", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])
            # Simplificamos o label para evitar erros de leitura do componente
            arq = st.file_uploader("Selecione a imagem do banner", type=['png', 'jpg', 'jpeg'])
            
            enviar = st.form_submit_button("ATIVAR PUBLICIDADE")
            
            if enviar:
                if cliente and link and arq:
                    try:
                        # Converte a imagem para Base64
                        img_b64 = base64.b64encode(arq.getvalue()).decode('utf-8')
                        
                        # GRAVAÇÃO NO BANCO VRS
                        db.collection("publicidade").add({
                            "cliente": cliente,
                            "link": link,
                            "estado_alvo": uf,
                            "foto": img_b64,
                            "data_cadastro": datetime.datetime.now()
                        })
                        st.success(f"✅ Banner de {cliente} ativado com sucesso!")
                        # Não damos rerun aqui para o usuário ver a mensagem de sucesso
                    except Exception as e:
                        st.error(f"❌ Erro ao gravar no banco: {e}")
                else:
                    st.warning("⚠️ Preencha todos os campos e selecione uma imagem.")

    st.markdown("---")
    st.subheader("📋 Banners Ativos")
    
    # Listagem de banners existentes
    try:
        banners_ref = db.collection("publicidade").order_by("data_cadastro", direction="DESCENDING").stream()
        lista_vazia = True
        
        for b in banners_ref:
            lista_vazia = False
            d = b.to_dict()
            with st.container(border=True):
                col_img, col_txt = st.columns([1, 2])
                with col_img:
                    st.image(f"data:image/jpeg;base64,{d['foto']}", use_container_width=True)
                with col_txt:
                    st.write(f"**Cliente:** {d['cliente']}")
                    st.write(f"**Alvo:** {d['estado_alvo']}")
                    if st.button("🗑️ Remover", key=f"del_{b.id}"):
                        db.collection("publicidade").document(b.id).delete()
                        st.rerun()
        
        if lista_vazia:
            st.info("Nenhum banner cadastrado no momento.")
            
    except Exception as e:
        st.caption(f"Aguardando novos banners... (Log: {e})")

def exibir_banner_rotativo_vrs(db, estado_atual="Brasil"):
    """Exibe o banner nacional no topo da vitrine."""
    try:
        # Busca banners com alvo 'Brasil' para alcance nacional
        query = db.collection("publicidade").where("estado_alvo", "==", "Brasil").stream()
        lista_banners = [b.to_dict() for b in query]
        
        if lista_banners:
            # Pega o banner mais recente
            banner = lista_banners[-1]
            
            # Injeta o HTML na interface
            st.markdown(f"""
                <div style="width:100%; margin-top: 10px; margin-bottom: 20px; text-align: center;">
                    <a href="{banner['link']}" target="_blank">
                        <img src="data:image/jpeg;base64,{banner['foto']}" 
                             style="width:100%; border-radius:10px; border: 1px solid #333; box-shadow: 0px 5px 15px rgba(0,0,0,0.3);">
                    </a>
                </div>
            """, unsafe_allow_html=True)
    except Exception:
        pass # Falha silenciosa para não quebrar a Home