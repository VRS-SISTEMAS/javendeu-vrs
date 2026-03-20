# =================================================================
# VRS SISTEMAS - JÁ VENDEU?
# MÓDULO: conexao.py (VERSÃO FINAL ABSOLUTA - ANTI-ERRO)
# =================================================================
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

def conectar_banco_vrs():
    if not firebase_admin._apps:
        try:
            if "firebase" in st.secrets:
                creds_dict = dict(st.secrets["firebase"])
                
                # A MÁGICA DA IARA: Reconstrói a chave perfeitamente
                pk = creds_dict["private_key"]
                
                # Remove qualquer tipo de lixo que o Streamlit inseriu
                pk = pk.replace("\\n", "\n").replace('"', '').replace("'", "").strip()
                
                # Garante o cabeçalho e rodapé oficiais
                if "-----BEGIN PRIVATE KEY-----" not in pk:
                    pk = "-----BEGIN PRIVATE KEY-----\n" + pk
                if "-----END PRIVATE KEY-----" not in pk:
                    pk = pk + "\n-----END PRIVATE KEY-----"
                
                creds_dict["private_key"] = pk
                
                cred = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(cred)
            else:
                cred = credentials.Certificate("vrs-solucoes-firebase-adminsdk.json")
                firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"❌ Erro de Conexão VRS: {e}")
            return None
    return firestore.client()