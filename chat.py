# =================================================================
# VRS SISTEMAS
# JÁ VENDEU? - GESTÃO DE CHAT INTEGRADO (ESTILO WHATSAPP)
# MÓDULO: chat.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import datetime

def exibir_interface_chat(db):
    """Renderiza a interface de mensagens WhatsApp Style."""
    if 'usuario' not in st.session_state or st.session_state['usuario'] is None:
        st.warning("⚠️ Por favor, faça login para acessar suas conversas.")
        return

    email_logado = st.session_state['usuario']['email']

    # Estilo Visual das Bolhas (WhatsApp Dark)
    st.markdown("""
        <style>
        .chat-vrs-bubble { display: flex; flex-direction: column; margin-bottom: 15px; width: 100%; }
        .balao-eu {
            align-self: flex-end; background-color: #056162; color: white; padding: 12px;
            border-radius: 15px 15px 0px 15px; max-width: 75%; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        }
        .balao-outro {
            align-self: flex-start; background-color: #262D31; color: white; padding: 12px;
            border-radius: 15px 15px 15px 0px; max-width: 75%; border: 1px solid #444;
        }
        .info-msg { font-size: 0.7rem; color: #aaa; margin-top: 5px; display: block; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: #FF4B4B;'>💬 MINHAS NEGOCIAÇÕES</h2>", unsafe_allow_html=True)

    try:
        # Busca mensagens envolvidas com o usuário atual (Exige índice no Firebase)
        msgs_ref = db.collection("mensagens_chat").where("envolvidos", "array_contains", email_logado).order_by("timestamp", direction="ASCENDING").stream()
        
        with st.container(height=500, border=True):
            encontradas = False
            for m in msgs_ref:
                encontradas = True
                msg = m.to_dict()
                sou_eu = msg['remetente_email'] == email_logado
                classe = "balao-eu" if sou_eu else "balao-outro"
                nome = "Você" if sou_eu else msg['remetente_nome']

                st.markdown(f"""
                    <div class="chat-vrs-bubble">
                        <div class="{classe}">
                            <b style='color: #FF4B4B; font-size: 0.85rem;'>{nome}</b><br>
                            {msg['texto']}
                            <span class="info-msg">{msg['hora']} - {msg.get('produto_ref', 'Geral')}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            if not encontradas:
                st.info("Nenhuma conversa ativa ainda. Inicie um interesse na Home!")

    except Exception as e:
        st.error(f"⚠️ Aguardando sincronização do chat no Firebase...")
        st.caption(f"Ref: {e}")

    st.markdown("---")

    # Campo de Envio Fixo
    if 'vrs_chat_ativo' in st.session_state:
        destinatario = st.session_state['vrs_chat_ativo']
        with st.form("form_msg_vrs", clear_on_submit=True):
            col_txt, col_btn = st.columns([8, 2])
            txt = col_txt.text_input("Escreva sua mensagem...")
            if col_btn.form_submit_button("ENVIAR 🚀"):
                if txt:
                    enviar_mensagem_vrs(db, destinatario, txt, st.session_state.get('vrs_produto_atual', 'Geral'))
                    st.rerun()
    else:
        st.caption("ℹ️ Selecione um produto na Vitrine e clique em 'Tenho Interesse' para conversar.")

def enviar_mensagem_vrs(db, destinatario_email, texto, produto_nome="Geral"):
    """Grava os dados da mensagem no Firestore."""
    email_logado = st.session_state['usuario']['email']
    nome_logado = st.session_state['usuario']['nome']
    db.collection("mensagens_chat").add({
        "texto": texto, 
        "remetente_email": email_logado, 
        "remetente_nome": nome_logado,
        "destinatario_email": destinatario_email, 
        "envolvidos": [email_logado, destinatario_email],
        "produto_ref": produto_nome, 
        "hora": datetime.datetime.now().strftime("%H:%M"),
        "timestamp": datetime.datetime.now()
    })