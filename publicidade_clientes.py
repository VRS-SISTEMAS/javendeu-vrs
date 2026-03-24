# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: publicidade_clientes.py (CARROSSEL AUTOMÁTICO 5s)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime
import io
import time
from PIL import Image

# Importante: Para o carrossel rodar sozinho no Streamlit, usamos o autorefresh
try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st.error("🚨 Execute 'pip install streamlit-autorefresh' no terminal para ativar o carrossel.")
    st.stop()

def gerenciar_banners_vrs(db):
    """Painel administrativo para o Vitor cadastrar publicidade paga."""
    st.subheader("🚀 Gestão de Banners")
    
    with st.expander("➕ Novo Banner de Cliente", expanded=False):
        cliente = st.text_input("Nome do Cliente", key="vrs_pub_nome")
        link = st.text_input("Link WhatsApp/Site", key="vrs_pub_link")
        uf = st.selectbox("Estado Alvo", ["Brasil", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"], key="vrs_pub_uf")
        arq = st.file_uploader("Upload do Banner", type=['png', 'jpg', 'jpeg'], key="vrs_pub_img")
        
        if st.button("✅ ATIVAR PUBLICIDADE", use_container_width=True):
            if cliente and link and arq:
                try:
                    img_original = Image.open(arq)
                    if img_original.mode in ('RGBA', 'LA', 'P'): img_original = img_original.convert('RGB')
                    
                    # Redimensionamento padrão VRS para ocupar a largura toda
                    img_redimensionada = img_original.resize((1200, 250), Image.Resampling.LANCZOS)
                    buffer = io.BytesIO()
                    img_redimensionada.save(buffer, format="JPEG", quality=85)
                    img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    
                    db.collection("publicidade").add({
                        "cliente": cliente, "link": link, "estado_alvo": uf,
                        "foto": img_b64, "data_cadastro": datetime.datetime.now()
                    })
                    st.success(f"✅ Banner de '{cliente}' ativado!")
                    st.rerun()
                except Exception as e: st.error(f"Erro: {e}")

    st.markdown("---")
    st.subheader("📋 Banners Ativos")
    try:
        banners = db.collection("publicidade").order_by("data_cadastro", direction="DESCENDING").stream()
        for b in banners:
            d = b.to_dict()
            with st.container(border=True):
                col1, col2 = st.columns([1, 2])
                with col1: st.image(f"data:image/jpeg;base64,{d['foto']}", use_container_width=True)
                with col2:
                    st.write(f"**{d['cliente']}** ({d['estado_alvo']})")
                    if st.button("🗑️ Remover", key=f"del_{b.id}"):
                        db.collection("publicidade").document(b.id).delete()
                        st.rerun()
    except: pass

def exibir_banner_rotativo_vrs(db, estado_atual="Brasil"):
    """
    EXIBIÇÃO EM CARROSSEL (TROCA A CADA 5 SEGUNDOS)
    LÓGICA: Puxa todos os banners 'Brasil' e faz o rodízio.
    """
    try:
        # 1. Busca todos os banners nacionais ativos
        query = db.collection("publicidade").where("estado_alvo", "==", "Brasil").stream()
        lista_banners = [b.to_dict() for b in query]
        
        if not lista_banners:
            return

        # 2. Configura o Auto-Refresh (5000ms = 5 segundos)
        # Isso faz a página atualizar silenciosamente para trocar o slide
        st_autorefresh(interval=5000, key="carrossel_vrs")

        # 3. Lógica de controle do Índice (qual banner mostrar agora)
        if 'index_banner_vrs' not in st.session_state:
            st.session_state.index_banner_vrs = 0
        else:
            st.session_state.index_banner_vrs = (st.session_state.index_banner_vrs + 1) % len(lista_banners)

        # Seleciona o banner atual baseado no índice
        banner_atual = lista_banners[st.session_state.index_banner_vrs]

        # 4. Renderização HTML com link e sombra
        st.markdown(f"""
            <div style="width:100%; margin-top: 5px; margin-bottom: 15px;">
                <a href="{banner_atual['link']}" target="_blank">
                    <img src="data:image/jpeg;base64,{banner_atual['foto']}" 
                         style="width:100%; border-radius:12px; border: 2px solid #333; 
                         box-shadow: 0px 6px 20px rgba(0,0,0,0.6); transition: 0.5s;">
                </a>
            </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        pass # Blindagem para não parar o site se o banco oscilar