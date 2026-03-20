# =================================================================
# VRS Soluções
# JÁ VENDEU? - CENTRAL DE CONEXÃO FIREBASE
# MÓDULO: conexao.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# AJUSTE: CORREÇÃO AUTOMÁTICA DA EXTENSÃO DUPLA
# =================================================================

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os

def conectar_banco_vrs():
    try:
        if firebase_admin._apps:
            return firestore.client()

        # Nomes possíveis devido à pegadinha do Windows
        caminho_correto = "vrs-solucoes-firebase-adminsdk.json"
        caminho_duplo = "vrs-solucoes-firebase-adminsdk.json.json"
        
        # Tenta achar o arquivo de qualquer jeito
        caminho_final = None
        if os.path.exists(caminho_correto):
            caminho_final = caminho_correto
        elif os.path.exists(caminho_duplo):
            caminho_final = caminho_duplo

        if caminho_final:
            cred = credentials.Certificate(caminho_final)
            firebase_admin.initialize_app(cred)
            return firestore.client()
        
        # Tenta Secrets se não achar arquivo local
        try:
            if "textkey" in st.secrets:
                cred_dict = dict(st.secrets["textkey"])
                pk = cred_dict["private_key"].replace("\\n", "\n").strip().strip('"').strip("'")
                cred_dict["private_key"] = pk
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
                return firestore.client()
        except:
            pass
            
        return None
        
    except Exception as e:
        st.error(f"Erro de Conexão VRS: {e}")
        return None

# --- FIM DO MÓDULO CONEXAO.PY ---