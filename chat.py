# =================================================================
# VRS SISTEMAS
# JÁ VENDEU? - GESTÃO DE CHAT TURBO (COM SELETOR E STATUS ONLINE)
# MÓDULO: chat.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import datetime

def exibir_interface_chat(db):
    """Renderiza a interface completa de chat com lista de contatos e status online."""
    if 'usuario' not in st.session_state or st.session_state['usuario'] is None:
        st.warning("⚠️ Por favor, faça login para acessar suas conversas.")
        return

    email_logado = st.session_state['usuario']['email']

    # --- ESTILIZAÇÃO AVANÇADA IARA ---
    st.markdown("""
        <style>
        .chat-vrs-bubble { display: flex; flex-direction: column; margin-bottom: 15px; width: 100%; }
        .balao-eu {
            align-self: flex-end; background-color: #056162; color: white; padding: 12px;
            border-radius: 15px 15px 0px 15px; max-width: 80%; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        }
        .balao-outro {
            align-self: flex-start; background-color: #262D31; color: white; padding: 12px;
            border-radius: 15px 15px 15px 0px; max-width: 80%; border: 1px solid #444;
        }
        .info-msg { font-size: 0.7rem; color: #aaa; margin-top: 5px; display: block; }
        
        /* Indicador Online */
        .status-online {
            color: #00FF00; font-size: 12px; font-weight: bold;
            display: flex; align-items: center; gap: 5px;
        }
        .ponto-verde {
            height: 10px; width: 10px; background-color: #00FF00;
            border-radius: 50%; display: inline-block;
        }
        </style>
    """, unsafe_allow_html=True)

    # CABEÇALHO COM STATUS ONLINE
    col_tit, col_status = st.columns([3, 1])
    with col_tit:
        st.markdown("<h2 style='color: #FF4B4B; margin:0;'>💬 NEGOCIAÇÕES</h2>", unsafe_allow_html=True)
    with col_status:
        st.markdown(f'<div class="status-online"><span class="ponto-verde"></span> ONLINE AGORA</div>', unsafe_allow_html=True)

    try:
        # 1. BUSCA TODAS AS MENSAGENS ONDE O USUÁRIO ESTÁ ENVOLVIDO
        msgs_ref = db.collection("mensagens_chat")\
                     .where("envolvidos", "array_contains", email_logado)\
                     .order_by("timestamp", direction="ASCENDING")\
                     .stream()
        
        lista_geral = [m.to_dict() for m in msgs_ref]

        if not lista_geral:
            st.info("👋 Nenhuma conversa ainda. Seus chats aparecerão aqui assim que alguém tiver interesse nos seus produtos!")
            return

        # 2. SEPARA OS CONTATOS (Quem conversou comigo)
        contatos = {} # Usar dict para guardar o nome junto
        for m in lista_geral:
            # Pega o e-mail da outra pessoa
            outro_email = m['envolvidos'][0] if m['envolvidos'][1] == email_logado else m['envolvidos'][1]
            # Pega o nome (se for remetente e não for eu, pega o nome)
            if m['remetente_email'] != email_logado:
                contatos[outro_email] = m['remetente_nome']
            elif outro_email not in contatos:
                contatos[outro_email] = "Interessado"

        # 3. LAYOUT DE DUAS COLUNAS (LISTA À ESQUERDA | CHAT À DIREITA)
        col_contatos, col_conversa = st.columns([1, 2.5])

        with col_contatos:
            st.markdown("### 👥 Contatos")
            for c_email, c_nome in contatos.items():
                if st.button(f"👤 {c_nome}\n({c_email})", key=f"btn_{c_email}", use_container_width=True):
                    st.session_state['vrs_chat_ativo'] = c_email
                    st.session_state['vrs_nome_ativo'] = c_nome
                    st.rerun()

        with col_conversa:
            if 'vrs_chat_ativo' in st.session_state:
                destinatario = st.session_state['vrs_chat_ativo']
                st.markdown(f"#### 🗨️ Conversa com {st.session_state.get('vrs_nome_ativo', destinatario)}")
                
                # Container de Mensagens
                with st.container(height=450, border=True):
                    for msg in lista_geral:
                        # Só mostra as mensagens entre eu e o contato selecionado
                        if destinatario in msg['envolvidos']:
                            sou_eu = msg['remetente_email'] == email_logado
                            classe = "balao-eu" if sou_eu else "balao-outro"
                            st.markdown(f"""
                                <div class="chat-vrs-bubble">
                                    <div class="{classe}">
                                        {msg['texto']}
                                        <span class="info-msg">{msg['hora']} - Ref: {msg.get('produto_ref', 'Geral')}</span>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

                # CAMPO DE RESPOSTA
                with st.form("form_resposta_vrs", clear_on_submit=True):
                    c_input, c_send = st.columns([8, 2])
                    msg_txt = c_input.text_input("Sua resposta...", placeholder="Digite aqui...")
                    if c_send.form_submit_button("ENVIAR 🚀", use_container_width=True):
                        if msg_txt:
                            enviar_mensagem_vrs(db, destinatario, msg_txt, "Resposta Direta")
                            st.rerun()
            else:
                st.markdown("""
                    <div style='text-align: center; margin-top: 100px; color: #666;'>
                        <h3>⬅️ Selecione um contato</h3>
                        <p>para ver o histórico e responder.</p>
                    </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error("🚨 ERRO DE SINCRONIZAÇÃO")
        st.write("Vitor, o chat está crescendo! Clique no link de índice no log do Streamlit se este erro persistir.")
        st.caption(f"Log: {e}")

def enviar_mensagem_vrs(db, destinatario_email, texto, produto_nome="Geral"):
    """Grava a mensagem garantindo os campos da VRS SISTEMAS."""
    if 'usuario' not in st.session_state: return
    
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