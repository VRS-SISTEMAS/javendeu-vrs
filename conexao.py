# =================================================================
# VRS SISTEMAS - JÁ VENDEU?
# MÓDULO: conexao.py (VERSÃO SUPREMA DE AUTO-REPARO)
# =================================================================
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

def conectar_banco_vrs():
    if not firebase_admin._apps:
        try:
            if "firebase" in st.secrets:
                creds_dict = dict(st.secrets["firebase"])
                
                # --- LIMPEZA DE ELITE DA IARA ---
                if "private_key" in creds_dict:
                    pk = creds_dict["private_key"]
                    # Troca o texto '\n' por quebra real e limpa espaços
                    pk = pk.replace("\\n", "\n").strip()
                    # Garante que as bordas do certificado estejam perfeitas
                    if not pk.startswith("-----BEGIN PRIVATE KEY-----"):
                        pk = "-----BEGIN PRIVATE KEY-----\n" + pk
                    if not pk.endswith("-----END PRIVATE KEY-----"):
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