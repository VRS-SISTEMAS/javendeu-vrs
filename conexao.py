# =================================================================
# VRS SISTEMAS - JÁ VENDEU?
# MÓDULO: conexao.py (VERSÃO SUPREMA - RESOLVE INVALIDLENGTH)
# =================================================================
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

def conectar_banco_vrs():
    if not firebase_admin._apps:
        try:
            # Se estivermos no Streamlit Cloud
            if "firebase" in st.secrets:
                creds_dict = {}
                for key, value in st.secrets["firebase"].items():
                    # Limpeza especial para a chave privada
                    if key == "private_key":
                        # Remove aspas e garante que os \n sejam quebras reais
                        value = value.replace("\\n", "\n").strip()
                        if value.startswith("'") or value.startswith('"'):
                            value = value[1:-1]
                    creds_dict[key] = value
                
                cred = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(cred)
            else:
                # Se estivermos no seu computador
                cred = credentials.Certificate("vrs-solucoes-firebase-adminsdk.json")
                firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"❌ Erro de Conexão VRS: {e}")
            return None
    return firestore.client()