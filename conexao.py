# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: conexao.py (VERSÃO SEGURA - SEM REFRESH)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

@st.cache_resource
def conectar_banco_vrs():
    if not firebase_admin._apps:
        try:
            if "firebase" in st.secrets:
                creds_dict = dict(st.secrets["firebase"])
                if "private_key" in creds_dict:
                    pk = creds_dict["private_key"].replace("\\n", "\n").strip()
                    creds_dict["private_key"] = pk
                
                cred = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(cred)
                return firestore.client()
            else:
                # Se estiver no seu PC local
                cred = credentials.Certificate("vrs-solucoes-firebase-adminsdk.json")
                firebase_admin.initialize_app(cred)
                return firestore.client()
        except Exception as e:
            st.error(f"Erro VRS: {e}")
            return None
    return firestore.client()

db = conectar_banco_vrs()