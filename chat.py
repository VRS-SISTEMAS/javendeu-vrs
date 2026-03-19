# =================================================================
# VRS Soluções - JÁ VENDEU? - MÓDULO: chat.py
# CHAT EM TEMPO REAL COM SUPORTE A ÍNDICES FIREBASE
# =================================================================
import streamlit as st
import datetime

def exibir_interface_chat(db):
    if 'usuario' not in st.session_state or st.session_state['usuario'] is None:
        st.warning("⚠️ Faça login para ver suas conversas.")
        return

    email_logado = st.session_state['usuario']['email']

    # Estilo Visual das Bolhas
    st.markdown("""
        <style>
        .balao-eu { align-self: flex-end; background-color: #056162; color: white; padding: 10px; border-radius: 10px 10px 0 10px; margin-bottom: 10px; text-align: right; }
        .balao-outro { align-self: flex-start; background-color: #262D31; color: white; padding: 10px; border-radius: 10px 10px 10px 0; margin-bottom: 10px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: #FF4B4B;'>💬 NEGOCIAÇÕES</h2>", unsafe_allow_html=True)

    try:
        # ATENÇÃO: É esta query que exige o índice no Firebase
        msgs_ref = db.collection("mensagens_chat").where("envolvidos", "array_contains", email_logado).order_by("timestamp", direction="ASCENDING").stream()
        
        with st.container(height=450, border=True):
            count = 0
            for m in msgs_ref:
                count += 1
                msg = m.to_dict()
                sou_eu = msg['remetente_email'] == email_logado
                classe = "balao-eu" if sou_eu else "balao-outro"
                nome = "Você" if sou_eu else msg['remetente_nome']

                st.markdown(f"<div class='{classe}'><b>{nome}</b><br>{msg['texto']}<br><small style='font-size: 10px;'>{msg['hora']} - {msg.get('produto_ref', '')}</small></div>", unsafe_allow_html=True)

            if count == 0:
                st.info("Nenhuma conversa por aqui ainda. Inicie um interesse na Home!")

    except Exception as e:
        # Se o índice ainda estiver sendo criado, ele mostra o link aqui
        st.error(f"Aguardando ativação do índice no Firebase...")
        st.caption(f"Detalhe: {e}")

    st.markdown("---")
    
    # Campo de envio fixo
    if 'vrs_chat_ativo' in st.session_state:
        with st.form("enviar_msg", clear_on_submit=True):
            txt = st.text_input("Sua mensagem:")
            if st.form_submit_button("ENVIAR 🚀"):
                if txt:
                    enviar_mensagem_vrs(db, st.session_state['vrs_chat_ativo'], txt, st.session_state.get('vrs_produto_atual', 'Geral'))
                    st.rerun()