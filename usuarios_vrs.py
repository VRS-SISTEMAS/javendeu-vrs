# =================================================================
# VRS Soluções
# JÁ VENDEU? - GESTÃO DE ACESSO (VERSÃO PERSISTENTE SEM BIBLIOTECAS)
# MÓDULO: usuarios_vrs.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import hashlib
import datetime
import re

def criar_hash(senha):
    """Cria uma assinatura digital da senha para segurança."""
    return hashlib.sha256(str.encode(senha)).hexdigest()

def validar_whatsapp_vrs(numero):
    """Valida se o número tem 11 dígitos (DDD + Celular)."""
    apenas_numeros = re.sub(r'\D', '', numero)
    return len(apenas_numeros) == 11

def gerenciar_acesso(db):
    """
    Controla o sistema de login e cadastro.
    Mantém o login ativo durante a sessão do navegador.
    """
    # Garante que as chaves de sessão existam
    if 'logado' not in st.session_state:
        st.session_state['logado'] = False
    if 'usuario' not in st.session_state:
        st.session_state['usuario'] = None

    if not st.session_state['logado']:
        with st.popover("👤 Logar / Cadastrar"):
            st.markdown("### Acesse sua conta VRS")
            tab_l, tab_c = st.tabs(["ENTRAR", "CADASTRAR"])
            
            with tab_l:
                e = st.text_input("E-mail", key="vrs_l_email")
                s = st.text_input("Senha (6 dígitos)", type="password", key="vrs_l_senha", max_chars=6)
                if st.button("ACESSAR SISTEMA", use_container_width=True):
                    if db:
                        user_ref = db.collection("usuarios").document(e).get()
                        if user_ref.exists and user_ref.to_dict()['senha'] == criar_hash(s):
                            # DEFINE LOGIN COMO VERDADEIRO
                            st.session_state['logado'] = True
                            st.session_state['usuario'] = user_ref.to_dict()
                            st.rerun()
                        else:
                            st.error("E-mail ou senha incorretos.")
            
            with tab_c:
                n = st.text_input("Nome Completo*", key="vrs_c_nome")
                em = st.text_input("E-mail*", key="vrs_c_email")
                col_seg1, col_seg2 = st.columns(2)
                cpf = col_seg1.text_input("CPF (11 dígitos)*", key="vrs_c_cpf", max_chars=11)
                zap = col_seg2.text_input("WhatsApp (11 dígitos)*", key="vrs_c_zap", max_chars=11)
                se = st.text_input("Senha (6 dígitos)*", type="password", key="vrs_c_senha", max_chars=6)
                
                if st.button("FINALIZAR CADASTRO SEGURO", use_container_width=True):
                    if n and em and len(se) == 6 and len(cpf) == 11 and validar_whatsapp_vrs(zap):
                        db.collection("usuarios").document(em).set({
                            "nome": n, "email": em, "cpf": cpf, "whatsapp": zap,
                            "senha": criar_hash(se), "data_cadastro": datetime.datetime.now()
                        })
                        st.success("Cadastro realizado! Faça login.")
                    else:
                        st.error("Verifique os campos obrigatórios.")

    else:
        # Interface logado - Exibe primeiro nome e botão sair
        nome_user = st.session_state['usuario']['nome'].split()[0].upper()
        with st.popover(f"✅ OLÁ, {nome_user}"):
            if st.button("📊 MEUS ANÚNCIOS", use_container_width=True):
                st.session_state['pagina_vrs'] = "Meus Anúncios"
                st.rerun()
            st.markdown("---")
            if st.button("SAIR DA CONTA", use_container_width=True):
                # Limpa tudo e desloga
                st.session_state['logado'] = False
                st.session_state['usuario'] = None
                st.session_state['pagina_vrs'] = "Home"
                st.rerun()

    return st.session_state['logado']