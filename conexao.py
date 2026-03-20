import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

def conectar_banco_vrs():
    if not firebase_admin._apps:
        try:
            # Tenta ler dos Secrets do Streamlit (Online)
            if "firebase" in st.secrets:
                creds_dict = dict(st.secrets["firebase"])
                cred = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(cred)
            else:
                # Se não achar segredos, tenta o arquivo local (Seu PC)
                cred = credentials.Certificate("vrs-solucoes-firebase-adminsdk.json")
                firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"❌ Erro de Conexão Firebase: {e}")
            return None
    return firestore.client()