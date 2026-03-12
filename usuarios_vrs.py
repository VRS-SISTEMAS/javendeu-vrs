# =================================================================
# VRS Soluções
# JÁ VENDEU? - GESTÃO DE USUÁRIOS E PRIVACIDADE
# MÓDULO: usuarios_vrs.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# AJUSTE: OTIMIZAÇÃO DE VELOCIDADE E CORREÇÃO DE STATUS
# =================================================================

import streamlit as st
import hashlib
import datetime
import time

def criar_hash(senha):
    """Cria um hash seguro para a senha do usuário."""
    return hashlib.sha256(str.encode(senha)).hexdigest()

def gerenciar_acesso(db):
    """Gerencia o login, logout e status online/offline do usuário."""
    # Inicializa o estado da sessão se não existir
    if 'logado' not in st.session_state:
        st.session_state['logado'] = False
        st.session_state['usuario'] = None

    if not st.session_state['logado']:
        with st.popover("👤 Minha Conta"):
            st.markdown("<span style='color: #888888;'>● Offline</span>", unsafe_allow_html=True)
            
            # Seletor de modo: Entrar ou Criar Conta
            modo = st.radio("Acesso", ["Entrar", "Criar Conta"], horizontal=True, label_visibility="collapsed")
            st.markdown("---")

            if modo == "Entrar":
                e = st.text_input("E-mail", key="login_email")
                s = st.text_input("Senha", type="password", key="login_senha")
                if st.button("LOGAR AGORA", use_container_width=True):
                    try:
                        # Busca o usuário no banco de dados da VRS Soluções
                        res = db.collection("usuarios").document(e).get()
                        if res.exists and res.to_dict()['senha'] == criar_hash(s):
                            st.session_state['logado'] = True
                            st.session_state['usuario'] = res.to_dict()
                            # Atualiza status para Online
                            db.collection("usuarios").document(e).update({
                                "status_vrs": "online", 
                                "ultima_atividade": datetime.datetime.now()
                            })
                            st.rerun()
                        else: 
                            st.error("Dados incorretos!")
                    except Exception: 
                        st.error("Erro de conexão. Tente novamente.")
            
            else:
                n = st.text_input("Nome completo", key="reg_nome")
                em = st.text_input("E-mail de acesso", key="reg_email")
                z = st.text_input("WhatsApp (com DDD)", key="reg_zap")
                se = st.text_input("Crie uma senha", type="password", key="reg_senha")
                p_zap = st.checkbox("Exibir WhatsApp nos anúncios?", value=False)
                
                if st.button("FINALIZAR CADASTRO", use_container_width=True):
                    if n and em and z and se:
                        sucesso = False
                        # Tenta gravar 3 vezes para garantir a persistência
                        for tentativa in range(3):
                            try:
                                db.collection("usuarios").document(em).set({
                                    "nome": n, 
                                    "email": em, 
                                    "zap": z, 
                                    "senha": criar_hash(se),
                                    "privacidade_zap": p_zap,
                                    "data": datetime.datetime.now(), 
                                    "status_vrs": "offline"
                                })
                                sucesso = True
                                break
                            except Exception:
                                time.sleep(1)
                        
                        if sucesso:
                            st.success("Conta criada! Mude para 'Entrar'.")
                        else:
                            st.error("Servidor ocupado. Tente de novo.")
                    else: 
                        st.warning("Preencha todos os campos!")
    else:
        # Usuário já está logado
        p_nome = st.session_state['usuario']['nome'].split()[0]
        with st.popover(f"✅ {p_nome}"):
            st.markdown("<span style='color: #00FF00;'>● Online</span>", unsafe_allow_html=True)
            if st.button("SAIR DA CONTA", use_container_width=True):
                try:
                    # Atualiza status para Offline ao sair
                    db.collection("usuarios").document(st.session_state['usuario']['email']).update({"status_vrs": "offline"})
                except Exception: 
                    pass
                st.session_state['logado'] = False
                st.session_state['usuario'] = None
                st.rerun()
            
    return st.session_state['logado']

def verificar_privacidade(vendedor_email, db):
    """Verifica se o vendedor autorizou mostrar o WhatsApp."""
    try:
        doc = db.collection("usuarios").document(vendedor_email).get()
        if doc.exists:
            return doc.to_dict().get("privacidade_zap", False)
    except Exception: 
        pass
    return False