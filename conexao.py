# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: conexao.py (VERSÃO RESTAURADA E SEGURA)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

@st.cache_resource
def conectar_banco_vrs():
    """Conecta ao Firebase usando Secrets (Online) ou JSON (Local)."""
    if not firebase_admin._apps:
        try:
            # 1. Tenta buscar nas Secrets do Streamlit (SITE ONLINE)
            if "firebase" in st.secrets:
                creds_dict = dict(st.secrets["firebase"])
                if "private_key" in creds_dict:
                    # Limpa a chave de qualquer sujeira de formatação
                    pk = creds_dict["private_key"].replace("\\n", "\n").replace('"', '').replace("'", "").strip()
                    creds_dict["private_key"] = pk
                
                cred = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(cred)
                return firestore.client()
            
            # 2. Se não achar Secrets, tenta o arquivo local (SEU PC)
            else:
                cred = credentials.Certificate("vrs-solucoes-firebase-adminsdk.json")
                firebase_admin.initialize_app(cred)
                return firestore.client()
                
        except Exception as e:
            st.error(f"❌ Erro de Conexão VRS: {e}")
            return None
    return firestore.client()

db = conectar_banco_vrs()