# =================================================================
# VRS SISTEMAS - JÁ VENDEU? - MÓDULO: conexao.py
# FUNÇÃO: CONEXÃO SEGURA HÍBRIDA (LOCAL E NUVEM)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

def conectar_banco_vrs():
    """Conecta ao Firebase usando arquivo local ou Secrets do Streamlit."""
    if not firebase_admin._apps:
        try:
            # 1. TENTA CONEXÃO VIA SECRETS (QUANDO ESTÁ ONLINE)
            if "firebase" in st.secrets:
                # Cria o dicionário de credenciais a partir dos segredos configurados
                creds_dict = {
                    "type": st.secrets["firebase"]["type"],
                    "project_id": st.secrets["firebase"]["project_id"],
                    "private_key_id": st.secrets["firebase"]["private_key_id"],
                    "private_key": st.secrets["firebase"]["private_key"],
                    "client_email": st.secrets["firebase"]["client_email"],
                    "client_id": st.secrets["firebase"]["client_id"],
                    "auth_uri": st.secrets["firebase"]["auth_uri"],
                    "token_uri": st.secrets["firebase"]["token_uri"],
                    "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
                    "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
                }
                cred = credentials.Certificate(creds_dict)
            else:
                # 2. TENTA CONEXÃO VIA ARQUIVO (QUANDO ESTÁ NO SEU PC)
                # Certifique-se que o nome do arquivo abaixo é o mesmo que você tem na pasta
                cred = credentials.Certificate("vrs-solucoes-firebase-adminsdk.json")
            
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Erro de conexão Firebase: {e}")
            return None
    return firestore.client()