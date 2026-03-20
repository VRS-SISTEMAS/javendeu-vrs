# =================================================================
# VRS SISTEMAS - JÁ VENDEU?
# MÓDULO: conexao.py (VERSÃO AUTO-CORREÇÃO)
# =================================================================
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os

def conectar_banco_vrs():
    if not firebase_admin._apps:
        try:
            # 1. TENTA LER DOS SECRETS (ONLINE)
            if "firebase" in st.secrets:
                creds_dict = dict(st.secrets["firebase"])
                
                # LIMPEZA TÉCNICA: Remove espaços ou caracteres de quebra de linha que bugam o PEM
                if "private_key" in creds_dict:
                    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
                
                cred = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(cred)
            
            # 2. TENTA LER LOCAL (SEU PC)
            else:
                caminho = "vrs-solucoes-firebase-adminsdk.json"
                if os.path.exists(caminho):
                    cred = credentials.Certificate(caminho)
                    firebase_admin.initialize_app(cred)
                else:
                    st.error("⚠️ Chave do Firebase não configurada corretamente.")
                    return None
        except Exception as e:
            st.error(f"❌ Erro de Conexão VRS SISTEMAS: {e}")
            return None
    return firestore.client()