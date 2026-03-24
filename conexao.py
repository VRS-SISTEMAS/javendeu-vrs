# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: conexao.py (VERSÃO RESTAURADA)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

@st.cache_resource
def conectar_banco_vrs():
    """Conexão blindada que reconstrói a chave privada da VRS SOLUÇÕES."""
    if not firebase_admin._apps:
        try:
            # PRIORIDADE 1: Secrets do Streamlit (Site Online)
            if "firebase" in st.secrets:
                creds_dict = dict(st.secrets["firebase"])
                pk = creds_dict.get("private_key", "")
                
                # Limpeza profunda da chave
                pk = pk.replace('\\n', '\n').replace('"', '').replace("'", "").strip()
                
                if "-----BEGIN PRIVATE KEY-----" in pk:
                    partes = pk.split("-----BEGIN PRIVATE KEY-----")
                    corpo_e_fim = partes[1].split("-----END PRIVATE KEY-----")
                    miolo = corpo_e_fim[0].replace("\n", "").replace(" ", "").strip()
                    pk = "-----BEGIN PRIVATE KEY-----\n" + miolo + "\n-----END PRIVATE KEY-----\n"
                
                creds_dict["private_key"] = pk
                cred = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(cred)
                return firestore.client()
            
            # PRIORIDADE 2: Local (PC do Vitor)
            else:
                cred = credentials.Certificate("vrs-solucoes-firebase-adminsdk.json")
                firebase_admin.initialize_app(cred)
                return firestore.client()
        except Exception as e:
            st.error(f"❌ Erro de Conexão VRS: {e}")
            return None
    return firestore.client()

db = conectar_banco_vrs()