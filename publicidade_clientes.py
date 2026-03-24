# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: publicidade_clientes.py (VERSÃO TANQUE DE GUERRA)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime
import io
import time
from PIL import Image

def gerenciar_banners_vrs(db):
    """Painel administrativo para o Vitor cadastrar publicidade."""
    st.subheader("🚀 Gestão de Banners - VRS Soluções")
    
    with st.expander("➕ Novo Banner de Cliente", expanded=False):
        cliente = st.text_input("Nome do Cliente", key="vrs_pub_nome")
        link = st.text_input("Link WhatsApp/Site", key="vrs_pub_link")
        uf = st.selectbox("Estado Alvo", ["Brasil", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"], key="vrs_pub_uf")
        arq = st.file_uploader("Upload do Banner", type=['png', 'jpg', 'jpeg'], key="vrs_pub_img")
        
        if st.button("✅ ATIVAR PUBLICIDADE", use_container_width=True):
            if cliente and link and arq:
                try:
                    # Processamento de imagem com padrão de qualidade VRS
                    img_original = Image.open(arq)
                    if img_original.mode in ('RGBA', 'LA', 'P'): 
                        img_original = img_original.convert('RGB')
                    
                    # Redimensionamento padrão para vitrine (1200x250)
                    img_redimensionada = img_original.resize((1200, 250), Image.Resampling.LANCZOS)
                    buffer = io.BytesIO()
                    img_redimensionada.save(buffer, format="JPEG", quality=85)
                    img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    
                    # Gravação no Banco de Dados
                    db.collection("publicidade").add({
                        "cliente": cliente, 
                        "link": link, 
                        "estado_alvo": uf,
                        "foto": img_b64, 
                        "data_cadastro": datetime.datetime.now()
                    })
                    st.success(f"✅ Banner de '{cliente}' ativado!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e: 
                    st.error(f"Erro ao cadastrar: {e}")

def exibir_banner_rotativo_vrs(db, estado_atual="Brasil"):
    """Exibição em carrossel nativo (Troca a cada 7 segundos)."""
    try:
        # Busca banners ativos (Filtro nacional por padrão)
        query = db.collection("publicidade").where("estado_alvo", "==", "Brasil").stream()
        lista_banners = [b.to_dict() for b in query]
        
        if not lista_banners:
            return

        # Rotação baseada no tempo do sistema (estratégia anti-travamento)
        indice = (int(time.time()) // 7) % len(lista_banners)
        banner = lista_banners[indice]

        # Renderização HTML com CSS estilizado para a VRS Soluções
        st.markdown(f"""
            <div style="width:100%; margin-top: 5px; margin-bottom: 15px;">
                <a href="{banner['link']}" target="_blank">
                    <img src="data:image/jpeg;base64,{banner['foto']}" 
                         style="width:100%; border-radius:12px; border: 1px solid #444; 
                         box-shadow: 0px 4px 15px rgba(0,0,0,0.5);">
                </a>
            </div>
        """, unsafe_allow_html=True)
    except Exception:
        # Blindagem: se o banco falhar, o app não cai, apenas oculta o banner
        pass