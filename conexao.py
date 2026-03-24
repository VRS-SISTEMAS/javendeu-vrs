# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: conexao.py (VERSÃO NOCAUTE - ANTI-INVALIDLENGTH)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# Usamos o cache para não ficar tentando conectar toda hora e travar
@st.cache_resource
def conectar_banco_vrs():
    """Conexão blindada que reconstrói a chave privada da VRS SOLUÇÕES."""
    if not firebase_admin._apps:
        try:
            # PRIORIDADE: Secrets do Streamlit (Site Online)
            if "firebase" in st.secrets:
                creds_dict = dict(st.secrets["firebase"])
                
                # RECONSTRUTOR MESTRE DA IARA (Limpeza Profunda)
                pk = creds_dict.get("private_key", "")
                
                # Remove sujeira de quebras de linha e aspas
                pk = pk.replace('\\n', '\n').replace('"', '').replace("'", "").strip()
                
                if "-----BEGIN PRIVATE KEY-----" in pk:
                    # Extrai o miolo da chave
                    partes = pk.split("-----BEGIN PRIVATE KEY-----")
                    corpo_e_fim = partes[1].split("-----END PRIVATE KEY-----")
                    miolo = corpo_e_fim[0].replace("\n", "").replace(" ", "").strip()
                    # Remonta no padrão que o Google exige
                    pk = "-----BEGIN PRIVATE KEY-----\n" + miolo + "\n-----END PRIVATE KEY-----\n"
                
                creds_dict["private_key"] = pk
                
                cred = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(cred)
                return firestore.client()
            
            else:
                # Se estiver rodando no seu PC (Local)
                try:
                    cred = credentials.Certificate("vrs-solucoes-firebase-adminsdk.json")
                    firebase_admin.initialize_app(cred)
                    return firestore.client()
                except:
                    st.error("❌ VRS: Chave do banco não encontrada (Secrets ou Local)!")
                    return None
                    
        except Exception as e:
            st.error(f"❌ Erro de Autenticação VRS: {e}")
            return None
            
    return firestore.client()

# --- SEGURANÇA VRS ---
# Em vez de chamar direto, criamos uma variável segura
db = conectar_banco_vrs()

if db is None:
    st.warning("⚠️ O sistema está operando sem conexão com o banco de dados.")