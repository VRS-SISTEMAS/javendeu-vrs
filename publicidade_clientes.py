# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: publicidade_clientes.py (SISTEMA DE BANNERS)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime
import time

def exibir_banner_rotativo_vrs(db, estado_atual="Brasil"):
    """Exibe o banner no topo da vitrine com rotação simples."""
    try:
        filtros = ["Brasil"]
        if estado_atual != "Brasil": filtros.append(estado_atual)
        
        query = db.collection("publicidade").where("estado_alvo", "in", filtros).stream()
        lista = [b.to_dict() for b in query]
        
        if lista:
            # Rotação simples baseada no tempo (muda a cada 10 segundos)
            idx = (int(time.time()) // 10) % len(lista)
            banner = lista[idx]
            
            st.markdown(f"""
                <div style="width:100%; margin-bottom: 20px; text-align:center;">
                    <a href="{banner['link']}" target="_blank">
                        <img src="data:image/jpeg;base64,{banner['foto']}" style="width:100%; border-radius:10px; max-height:250px; object-fit:cover;">
                    </a>
                </div>
            """, unsafe_allow_html=True)
    except:
        pass