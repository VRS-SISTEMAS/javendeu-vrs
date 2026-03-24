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
    """
    Painel administrativo para o Vitor cadastrar publicidade paga.
    Garante que as imagens sejam salvas no formato correto e redimensionadas.
    """
    st.subheader("🚀 Gestão de Banners - VRS Soluções")
    
    with st.expander("➕ Novo Banner de Cliente", expanded=False):
        cliente = st.text_input("Nome do Cliente", key="vrs_pub_nome")
        link = st.text_input("Link WhatsApp/Site", key="vrs_pub_link")
        uf = st.selectbox("Estado Alvo", ["Brasil", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"], key="vrs_pub_uf")
        arq = st.file_uploader("Upload do Banner (Recomendado: 1200x250)", type=['png', 'jpg', 'jpeg'], key="vrs_pub_img")
        
        if st.button("✅ ATIVAR PUBLICIDADE", use_container_width=True):
            if cliente and link and arq:
                try:
                    # Tratamento de imagem padrão VRS
                    img_original = Image.open(arq)
                    if img_original.mode in ('RGBA', 'LA', 'P'): 
                        img_original = img_original.convert('RGB')
                    
                    # Redimensionamento para manter o padrão visual da plataforma
                    img_redimensionada = img_original.resize((1200, 250), Image.Resampling.LANCZOS)
                    buffer = io.BytesIO()
                    img_redimensionada.save(buffer, format="JPEG", quality=85)
                    img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    
                    # Cadastro no banco de dados Firebase
                    db.collection("publicidade").add({
                        "cliente": cliente, 
                        "link": link, 
                        "estado_alvo": uf,
                        "foto": img_b64, 
                        "data_cadastro": datetime.datetime.now()
                    })
                    st.success(f"✅ Banner de '{cliente}' ativado com sucesso!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e: 
                    st.error(f"Erro ao processar banner: {e}")

    st.markdown("---")
    st.subheader("📋 Banners Ativos")
    try:
        banners = db.collection("publicidade").order_by("data_cadastro", direction="DESCENDING").stream()
        for b in banners:
            d = b.to_dict()
            with st.container(border=True):
                col1, col2 = st.columns([1, 2])
                with col1: 
                    st.image(f"data:image/jpeg;base64,{d['foto']}", use_container_width=True)
                with col2:
                    st.write(f"**{d['cliente']}** ({d['estado_alvo']})")
                    if st.button("🗑️ Remover Banner", key=f"del_{b.id}"):
                        db.collection("publicidade").document(b.id).delete()
                        st.rerun()
    except Exception:
        st.info("Aguardando carregamento de banners...")

def exibir_banner_rotativo_vrs(db, estado_atual="Brasil"):
    """
    EXIBIÇÃO EM CARROSSEL (RODÍZIO AUTOMÁTICO)
    LÓGICA: Alterna entre os anúncios 'Brasil' a cada 5 segundos.
    """
    # Criamos um espaço vazio para o banner não "pular" na tela
    espaco_banner = st.empty()
    
    try:
        # Busca banners ativos para o Brasil
        query = db.collection("publicidade").where("estado_alvo", "==", "Brasil").stream()
        lista_banners = [b.to_dict() for b in query]
        
        if not lista_banners:
            return

        # Lógica de tempo para selecionar o banner (Troca a cada 5s)
        # Usamos o tempo do Unix dividido pelo intervalo para definir o índice
        intervalo = 5
        indice = (int(time.time()) // intervalo) % len(lista_banners)
        banner = lista_banners[indice]

        # Renderização HTML elegante com o padrão de sombras da VRS Soluções
        with espaco_banner.container():
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
        # Se algo falhar, o espaço fica vazio para não travar o site principal
        espaco_banner.empty()