# =================================================================
# VRS SISTEMAS - JÁ VENDEU?
# MÓDULO: conexao.py (VERSÃO SUPREMA ANTI-ERRO)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

def conectar_banco_vrs():
    """Conecta ao Firebase garantindo a limpeza da chave privada da VRS SISTEMAS."""
    if not firebase_admin._apps:
        try:
            # 1. TENTA CONEXÃO VIA SECRETS (STREAMLIT CLOUD)
            if "firebase" in st.secrets:
                creds_dict = dict(st.secrets["firebase"])
                
                # --- LIMPEZA DE ELITE DA IARA ---
                pk = creds_dict.get("private_key", "")
                
                # Remove aspas malucas, espaços e trata as quebras de linha
                pk = pk.replace("\\n", "\n").replace('"', '').replace("'", "").strip()
                
                # Garante que as bordas do certificado estejam intactas
                if "-----BEGIN PRIVATE KEY-----" not in pk:
                    pk = "-----BEGIN PRIVATE KEY-----\n" + pk
                if "-----END PRIVATE KEY-----" not in pk:
                    pk = pk + "\n-----END PRIVATE KEY-----"
                
                creds_dict["private_key"] = pk
                # -------------------------------

                cred = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(cred)
            
            # 2. TENTA CONEXÃO LOCAL (SEU COMPUTADOR)
            else:
                cred = credentials.Certificate("vrs-solucoes-firebase-adminsdk.json")
                firebase_admin.initialize_app(cred)
                
        except Exception as e:
            st.error(f"❌ Erro de Conexão VRS: {e}")
            return None
            
    return firestore.client()