# =================================================================
# VRS SISTEMAS - JÁ VENDEU?
# MÓDULO: conexao.py (VERSÃO BLINDADA CONTRA ERROS DE PEM)
# =================================================================
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os

def conectar_banco_vrs():
    if not firebase_admin._apps:
        try:
            if "firebase" in st.secrets:
                # Criamos uma cópia para não mexer no original
                creds_dict = dict(st.secrets["firebase"])
                
                # --- LIMPEZA BRAVA DA IARA ---
                raw_key = creds_dict.get("private_key", "")
                
                # 1. Troca o texto '\n' por quebras de linha reais
                # 2. Remove espaços sobrando no início e fim
                # 3. Garante que as bordas do certificado existam
                clean_key = raw_key.replace("\\n", "\n").strip()
                
                if "-----BEGIN PRIVATE KEY-----" not in clean_key:
                    clean_key = "-----BEGIN PRIVATE KEY-----\n" + clean_key
                if "-----END PRIVATE KEY-----" not in clean_key:
                    clean_key = clean_key + "\n-----END PRIVATE KEY-----"
                
                creds_dict["private_key"] = clean_key
                # -----------------------------

                cred = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(cred)
            else:
                caminho = "vrs-solucoes-firebase-adminsdk.json"
                if os.path.exists(caminho):
                    cred = credentials.Certificate(caminho)
                    firebase_admin.initialize_app(cred)
                else:
                    st.error("⚠️ Secrets não configurados.")
                    return None
        except Exception as e:
            st.error(f"❌ Erro de Conexão VRS SISTEMAS: {e}")
            return None
    return firestore.client()