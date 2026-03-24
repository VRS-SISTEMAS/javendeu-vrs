# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: conexao.py (VERSÃO NOCAUTE - ANTI-INVALIDLENGTH)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

def conectar_banco_vrs():
    """Conexão blindada que reconstrói a chave privada da VRS SOLUÇÕES."""
    if not firebase_admin._apps:
        try:
            # PRIORIDADE 1: Secrets do Streamlit (Site Online)
            if "firebase" in st.secrets:
                creds_dict = dict(st.secrets["firebase"])
                
                # RECONSTRUTOR MESTRE DA IARA (Limpeza Profunda)
                pk = creds_dict.get("private_key", "")
                
                # Remove aspas extras que o Streamlit às vezes coloca e limpa espaços
                pk = pk.replace('\\n', '\n').strip()
                
                # Garante que a chave comece e termine corretamente sem lixo em volta
                if "-----BEGIN PRIVATE KEY-----" in pk:
                    # Extrai apenas o que está entre os marcadores se houver sujeira
                    partes = pk.split("-----BEGIN PRIVATE KEY-----")
                    corpo_e_fim = partes[1].split("-----END PRIVATE KEY-----")
                    miolo = corpo_e_fim[0].replace("\n", "").replace(" ", "")
                    # Remonta do jeito que o Firebase ama
                    pk = "-----BEGIN PRIVATE KEY-----\n" + miolo + "\n-----END PRIVATE KEY-----\n"
                
                creds_dict["private_key"] = pk
                
                cred = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(cred)
                
            else:
                # PRIORIDADE 2: Local (Apenas para o PC do Vitor)
                try:
                    cred = credentials.Certificate("vrs-solucoes-firebase-adminsdk.json")
                    firebase_admin.initialize_app(cred)
                except:
                    st.error("❌ ERRO CRÍTICO: Chave do banco não encontrada nas Secrets nem localmente!")
                    return None
                    
        except Exception as e:
            st.error(f"❌ Erro de Autenticação VRS: {e}")
            return None
            
    return firestore.client()

# Instância global para ser usada em todo o sistema Já Vendeu?
db = conectar_banco_vrs()