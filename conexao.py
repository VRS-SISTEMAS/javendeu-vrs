# =================================================================
# VRS SISTEMAS
# JÁ VENDEU? - MÓDULO: conexao.py (CONEXÃO HÍBRIDA SEGURA)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os

def conectar_banco_vrs():
    """Gerencia a conexão com o Firebase protegendo as chaves da VRS SISTEMAS."""
    if not firebase_admin._apps:
        try:
            # 1. TENTA CONEXÃO VIA SECRETS (QUANDO ESTÁ ONLINE NO STREAMLIT)
            if "firebase" in st.secrets:
                # O dict(st.secrets["firebase"]) pega todos os campos que você colou lá
                creds_dict = dict(st.secrets["firebase"])
                cred = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(cred)
            
            # 2. TENTA CONEXÃO VIA ARQUIVO LOCAL (QUANDO ESTÁ NO SEU PC)
            else:
                caminho_local = "vrs-solucoes-firebase-adminsdk.json"
                if os.path.exists(caminho_local):
                    cred = credentials.Certificate(caminho_local)
                    firebase_admin.initialize_app(cred)
                else:
                    st.error("⚠️ Chave do Firebase não encontrada (Arquivo ou Secrets).")
                    return None
                    
        except Exception as e:
            # Mostra o erro exato na tela para sabermos o que corrigir
            st.error(f"❌ Erro de Conexão VRS SISTEMAS: {e}")
            return None
            
    return firestore.client()