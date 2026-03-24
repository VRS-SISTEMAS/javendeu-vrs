# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: publicidade_clientes.py (FORÇAR GRAVAÇÃO NO BANCO)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime

def gerenciar_banners_vrs(db):
    """Painel para o Vitor cadastrar publicidade paga."""
    st.subheader("🚀 Gestão de Banners")
    
    # Formulário de Cadastro
    with st.expander("➕ Novo Banner de Cliente", expanded=True):
        # Removi o st.form para testar a gravação direta, que é mais estável para uploads
        cliente = st.text_input("Nome do Cliente", key="vrs_pub_nome")
        link = st.text_input("Link (Site ou WhatsApp)", key="vrs_pub_link")
        uf = st.selectbox("Estado Alvo", ["Brasil", "RJ", "SP", "MG", "ES", "BA", "PR", "SC", "RS"], key="vrs_pub_uf")
        arq = st.file_uploader("Selecione a imagem (1200x200px)", type=['png', 'jpg', 'jpeg'], key="vrs_pub_img")
        
        if st.button("✅ ATIVAR PUBLICIDADE AGORA", use_container_width=True):
            if cliente and link and arq:
                try:
                    # Converte a imagem
                    img_data = arq.getvalue()
                    img_b64 = base64.b64encode(img_data).decode('utf-8')
                    
                    # Dados para o banco
                    dados_banner = {
                        "cliente": cliente,
                        "link": link,
                        "estado_alvo": uf,
                        "foto": img_b64,
                        "data_cadastro": datetime.datetime.now()
                    }
                    
                    # GRAVAÇÃO DIRETA NO FIREBASE
                    db.collection("publicidade").add(dados_banner)
                    
                    st.success(f"Banner de '{cliente}' gravado com sucesso!")
                    st.rerun() # Força a atualização do contador para sair do 0
                except Exception as e:
                    st.error(f"Erro técnico ao salvar: {e}")
            else:
                st.warning("Preencha todos os campos antes de ativar.")

    st.markdown("---")
    st.subheader("📋 Banners Ativos no Sistema")
    
    # Listagem de Banners para conferência
    try:
        banners_ref = db.collection("publicidade").order_by("data_cadastro", direction="DESCENDING").stream()
        tem_banner = False
        for b in banners_ref:
            tem_banner = True
            d = b.to_dict()
            with st.container(border=True):
                col_capa, col_info = st.columns([1, 2])
                with col_capa:
                    st.image(f"data:image/jpeg;base64,{d['foto']}", use_container_width=True)
                with col_info:
                    st.write(f"**Cliente:** {d['cliente']}")
                    st.write(f"**Alvo:** {d['estado_alvo']}")
                    if st.button("🗑️ Remover", key=f"del_{b.id}"):
                        db.collection("publicidade").document(b.id).delete()
                        st.rerun()
        if not tem_banner:
            st.info("Nenhum banner encontrado no banco de dados.")
    except:
        pass

def exibir_banner_rotativo_vrs(db, estado_atual="Brasil"):
    """Busca o banner nacional e exibe na interface principal."""
    try:
        # Busca apenas banners marcados como Brasil
        banners = db.collection("publicidade").where("estado_alvo", "==", "Brasil").stream()
        lista = [b.to_dict() for b in banners]
        
        if lista:
            # Pega o mais recente
            banner = lista[-1]
            st.markdown(f"""
                <div style="width:100%; margin-top: 10px; margin-bottom: 20px;">
                    <a href="{banner['link']}" target="_blank">
                        <img src="data:image/jpeg;base64,{banner['foto']}" 
                             style="width:100%; border-radius:10px; border: 1px solid #333; box-shadow: 0px 4px 12px rgba(0,0,0,0.4);">
                    </a>
                </div>
            """, unsafe_allow_html=True)
    except:
        pass