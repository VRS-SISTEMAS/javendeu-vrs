# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: publicidade_clientes.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import time

def exibir_banner_rotativo_vrs(db, estado_atual="Brasil"):
    """Exibição simples e segura sem bibliotecas externas."""
    try:
        # Busca banners no Firebase
        docs = db.collection("publicidade").where("estado_alvo", "==", "Brasil").stream()
        lista = [d.to_dict() for d in docs]
        
        if not lista:
            return

        # Rotação simples baseada no relógio
        indice = (int(time.time()) // 7) % len(lista)
        banner = lista[indice]

        st.markdown(f"""
            <div style="width:100%; text-align:center;">
                <a href="{banner['link']}" target="_blank">
                    <img src="data:image/jpeg;base64,{banner['foto']}" style="width:100%; border-radius:10px;">
                </a>
            </div>
        """, unsafe_allow_html=True)
    except:
        pass