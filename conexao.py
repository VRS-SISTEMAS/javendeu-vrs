# =================================================================
# VRS SISTEMAS - JÁ VENDEU?
# MÓDULO: conexao.py (VERSÃO FINAL ANTI-PADDYNG)
# =================================================================
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

def conectar_banco_vrs():
    if not firebase_admin._apps:
        try:
            if "firebase" in st.secrets:
                creds_dict = dict(st.secrets["firebase"])
                # Limpeza de segurança para evitar o erro InvalidPadding
                if "private_key" in creds_dict:
                    # Remove aspas extras e garante que as quebras sejam reais
                    key = creds_dict["private_key"].replace("\\n", "\n").strip()
                    if key.startswith("'") or key.startswith('"'):
                        key = key[1:-1]
                    creds_dict["private_key"] = key
                
                cred = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(cred)
            else:
                cred = credentials.Certificate("vrs-solucoes-firebase-adminsdk.json")
                firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"❌ Erro de Conexão VRS: {e}")
            return None
    return firestore.client()