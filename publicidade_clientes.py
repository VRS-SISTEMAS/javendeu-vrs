# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: publicidade_clientes.py (VERSÃO ESTABILIZADA)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime
import io
import time
from PIL import Image

def gerenciar_banners_vrs(db):
    st.subheader("🚀 Gestão de Banners - VRS Soluções")
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
                    img_redimensionada = img_original.resize((1200, 250), Image.Resampling.LANCZOS)
                    buffer = io.BytesIO()
                    img_redimensionada.save(buffer, format="JPEG", quality=85)
                    img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    db.collection("publicidade").add({
                        "cliente": cliente, "link": link, "estado_alvo": uf,
                        "foto": img_b64, "data_cadastro": datetime.datetime.now()
                    })
                    st.success("✅ Banner ativado!")
                    st.rerun()
                except Exception as e: st.error(f"Erro: {e}")

def exibir_banner_rotativo_vrs(db, estado_atual="Brasil"):
    try:
        query = db.collection("publicidade").where("estado_alvo", "==", "Brasil").stream()
        lista_banners = [b.to_dict() for b in query]
        if not lista_banners: return

        # Carrossel Nativo baseado no relógio (5 segundos)
        indice = (int(time.time()) // 5) % len(lista_banners)
        banner = lista_banners[indice]

        st.markdown(f"""
            <div style="width:100%; margin-top: 5px; margin-bottom: 15px;">
                <a href="{banner['link']}" target="_blank">
                    <img src="data:image/jpeg;base64,{banner['foto']}" 
                         style="width:100%; border-radius:12px; border: 1px solid #444; 
                         box-shadow: 0px 4px 15px rgba(0,0,0,0.5);">
                </a>
            </div>
        """, unsafe_allow_html=True)
    except: pass