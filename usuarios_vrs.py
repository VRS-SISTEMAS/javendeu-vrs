# =================================================================
# VRS Soluções
# JÁ VENDEU? - GESTÃO DE USUÁRIOS E PRIVACIDADE
# MÓDULO: usuarios_vrs.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# AJUSTE: CONTROLE DE PRIVACIDADE DO WHATSAPP NO CADASTRO
# =================================================================

import streamlit as st
import hashlib
import datetime

def criar_hash(senha):
    return hashlib.sha256(str.encode(senha)).hexdigest()

def gerenciar_acesso(db):
    if 'logado' not in st.session_state:
        st.session_state['logado'] = False
        st.session_state['usuario'] = None

    if not st.session_state['logado']:
        with st.popover("👤 Minha Conta"):
            st.markdown("<span style='color: #888888;'>● Offline</span>", unsafe_allow_html=True)
            aba = st.radio("Acesso", ["Entrar", "Criar Conta"], horizontal=True, label_visibility="collapsed")
            
            if aba == "Entrar":
                e = st.text_input("E-mail", key="vrs_e")
                s = st.text_input("Senha", type="password", key="vrs_s")
                if st.button("LOGAR", use_container_width=True):
                    res = db.collection("usuarios").document(e).get()
                    if res.exists and res.to_dict()['senha'] == criar_hash(s):
                        st.session_state['logado'] = True
                        st.session_state['usuario'] = res.to_dict()
                        db.collection("usuarios").document(e).update({
                            "status_vrs": "online", "ultima_atividade": datetime.datetime.now()
                        })
                        st.rerun()
                    else: st.error("Erro!")
            else:
                n = st.text_input("Nome")
                em = st.text_input("E-mail")
                z = st.text_input("Zap")
                se = st.text_input("Senha", type="password")
                # REGRA DE PRIVACIDADE NO CADASTRO
                p_zap = st.checkbox("Sempre exibir meu WhatsApp publicamente?", value=False)
                
                if st.button("CADASTRAR", use_container_width=True):
                    if n and em and z and se:
                        db.collection("usuarios").document(em).set({
                            "nome": n, "email": em, "zap": z, "senha": criar_hash(se),
                            "privacidade_zap": p_zap,
                            "data": datetime.datetime.now(), "status_vrs": "offline"
                        })
                        st.success("Criado!")
    else:
        p_nome = st.session_state['usuario']['nome'].split()[0]
        with st.popover(f"✅ {p_nome}"):
            st.markdown("<span style='color: #00FF00;'>● Online</span>", unsafe_allow_html=True)
            if st.button("SAIR DA CONTA", use_container_width=True):
                db.collection("usuarios").document(st.session_state['usuario']['email']).update({"status_vrs": "offline"})
                st.session_state['logado'] = False
                st.session_state['usuario'] = None
                st.rerun()
            
    return st.session_state['logado']

def verificar_privacidade(vendedor_email, db):
    """Verifica se o dono do anúncio permite mostrar o celular."""
    doc = db.collection("usuarios").document(vendedor_email).get()
    if doc.exists:
        return doc.to_dict().get("privacidade_zap", False)
    return False