# =================================================================
# VRS Soluções
# JÁ VENDEU? - GESTÃO DE USUÁRIOS E PRIVACIDADE
# MÓDULO: usuarios_vrs.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# AJUSTE: CORREÇÃO DE VISUAL ENCAVALADO E BLINDAGEM DE CADASTRO
# =================================================================

import streamlit as st
import hashlib
import datetime
import time

def criar_hash(senha):
    return hashlib.sha256(str.encode(senha)).hexdigest()

def gerenciar_acesso(db):
    if 'logado' not in st.session_state:
        st.session_state['logado'] = False
        st.session_state['usuario'] = None

    if not st.session_state['logado']:
        with st.popover("👤 Minha Conta"):
            st.markdown("<span style='color: #888888;'>● Offline</span>", unsafe_allow_html=True)
            aba = st.tabs(["Entrar", "Criar Conta"])
            
            with aba[0]:
                e = st.text_input("E-mail", key="vrs_e_login")
                s = st.text_input("Senha", type="password", key="vrs_s_login")
                if st.button("LOGAR", use_container_width=True):
                    try:
                        res = db.collection("usuarios").document(e).get()
                        if res.exists and res.to_dict()['senha'] == criar_hash(s):
                            st.session_state['logado'] = True
                            st.session_state['usuario'] = res.to_dict()
                            db.collection("usuarios").document(e).update({
                                "status_vrs": "online", "ultima_atividade": datetime.datetime.now()
                            })
                            st.rerun()
                        else: st.error("E-mail ou senha incorretos!")
                    except: st.error("Erro de conexão. Tente novamente.")
            
            with aba[1]:
                n = st.text_input("Nome completo", key="reg_n")
                em = st.text_input("E-mail de acesso", key="reg_e")
                z = st.text_input("WhatsApp (com DDD)", key="reg_z")
                se = st.text_input("Crie uma senha", type="password", key="reg_s")
                p_zap = st.checkbox("Exibir WhatsApp nos anúncios?", value=False)
                
                if st.button("FINALIZAR CADASTRO", use_container_width=True):
                    if n and em and z and se:
                        sucesso = False
                        # Tenta gravar 3 vezes para evitar o Retry Error do servidor
                        for tentativa in range(3):
                            try:
                                db.collection("usuarios").document(em).set({
                                    "nome": n, "email": em, "zap": z, "senha": criar_hash(se),
                                    "privacidade_zap": p_zap,
                                    "data": datetime.datetime.now(), "status_vrs": "offline"
                                })
                                sucesso = True
                                break
                            except:
                                time.sleep(1)
                        
                        if sucesso:
                            st.success("Conta criada! Vá na aba 'Entrar'.")
                        else:
                            st.error("Servidor instável. Tente novamente.")
                    else: st.warning("Preencha todos os campos!")
    else:
        p_nome = st.session_state['usuario']['nome'].split()[0]
        with st.popover(f"✅ {p_nome}"):
            st.markdown("<span style='color: #00FF00;'>● Online</span>", unsafe_allow_html=True)
            if st.button("SAIR DA CONTA", use_container_width=True):
                try:
                    db.collection("usuarios").document(st.session_state['usuario']['email']).update({"status_vrs": "offline"})
                except: pass
                st.session_state['logado'] = False
                st.session_state['usuario'] = None
                st.rerun()
            
    return st.session_state['logado']

def verificar_privacidade(vendedor_email, db):
    try:
        doc = db.collection("usuarios").document(vendedor_email).get()
        if doc.exists:
            return doc.to_dict().get("privacidade_zap", False)
    except: pass
    return False