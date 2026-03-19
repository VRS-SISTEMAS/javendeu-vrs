# =================================================================
# VRS Soluções
# JÁ VENDEU? - GESTÃO DE ACESSO (LOGIN COMPACTO)
# MÓDULO: usuarios_vrs.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import hashlib
import datetime

def criar_hash(senha):
    """Cria uma assinatura digital da senha para segurança."""
    return hashlib.sha256(str.encode(senha)).hexdigest()

def gerenciar_acesso(db):
    """
    Controla o sistema de login e cadastro em um popover.
    Gerencia estados 'logado' e 'usuario'.
    """
    # Inicializa estados se não existirem
    if 'logado' not in st.session_state:
        st.session_state['logado'] = False
        st.session_state['usuario'] = None

    # Caso não esteja logado
    if not st.session_state['logado']:
        with st.popover("👤 Logar"):
            st.markdown("### Acesse sua conta")
            tab_l, tab_c = st.tabs(["ENTRAR", "CADASTRAR"])
            
            with tab_l:
                e = st.text_input("E-mail", key="vrs_l_email")
                s = st.text_input("Senha (6 dígitos)", type="password", key="vrs_l_senha", max_chars=6)
                if st.button("ACESSAR", use_container_width=True):
                    if db:
                        user_ref = db.collection("usuarios").document(e).get()
                        if user_ref.exists and user_ref.to_dict()['senha'] == criar_hash(s):
                            st.session_state['logado'] = True
                            st.session_state['usuario'] = user_ref.to_dict()
                            st.rerun()
                        else:
                            st.error("Dados inválidos.")
            
            with tab_c:
                n = st.text_input("Nome Completo", key="vrs_c_nome")
                em = st.text_input("E-mail", key="vrs_c_email")
                se = st.text_input("Senha (6 dígitos)", type="password", key="vrs_c_senha", max_chars=6)
                if st.button("FINALIZAR CADASTRO", use_container_width=True):
                    if n and em and len(se) == 6:
                        db.collection("usuarios").document(em).set({
                            "nome": n, "email": em, "senha": criar_hash(se),
                            "data_cadastro": datetime.datetime.now()
                        })
                        st.success("Cadastro realizado!")

    else:
        # Interface logado
        nome_user = st.session_state['usuario']['nome'].split()[0]
        with st.popover(f"✅ {nome_user}"):
            if st.button("📊 MEUS ANÚNCIOS", use_container_width=True):
                st.session_state['pagina_vrs'] = "Meus Anúncios"
                st.rerun()
            st.markdown("---")
            if st.button("SAIR", use_container_width=True):
                st.session_state['logado'] = False
                st.session_state['usuario'] = None
                st.session_state['pagina_vrs'] = "Home"
                st.rerun()

    return st.session_state['logado']