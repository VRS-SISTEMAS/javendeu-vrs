# =================================================================
# VRS SISTEMAS
# JÁ VENDEU? - GESTÃO DE CHAT TURBO (CAMPANHA, SELETOR E EXCLUSÃO)
# MÓDULO: chat.py
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import datetime
import streamlit.components.v1 as components

def tocar_campainha_vrs():
    """Injeta JavaScript para tocar som de notificação."""
    # Som de alerta profissional (Ping)
    audio_url = "https://www.soundjay.com/buttons/beep-07a.mp3"
    components.html(
        f"""
        <audio autoplay>
            <source src="{audio_url}" type="audio/mp3">
        </audio>
        """,
        height=0,
    )

def exibir_interface_chat(db):
    """Renderiza a interface completa de chat com lista de contatos, alerta e exclusão."""
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
        
        lista_geral = []
        for m in msgs_ref:
            d = m.to_dict()
            d['id'] = m.id # Guarda o ID do documento para exclusão
            lista_geral.append(d)

        # --- LÓGICA DA CAMPAINHA ---
        if 'vrs_total_msgs' not in st.session_state:
            st.session_state['vrs_total_msgs'] = len(lista_geral)
        
        if len(lista_geral) > st.session_state['vrs_total_msgs']:
            if lista_geral[-1]['remetente_email'] != email_logado:
                tocar_campainha_vrs()
            st.session_state['vrs_total_msgs'] = len(lista_geral)

        if not lista_geral:
            st.info("👋 Nenhuma conversa ainda. Seus chats aparecerão aqui assim que alguém tiver interesse!")
            return

        # 2. SEPARA OS CONTATOS
        contatos = {}
        for m in lista_geral:
            outro_email = m['envolvidos'][0] if m['envolvidos'][1] == email_logado else m['envolvidos'][1]
            if m['remetente_email'] != email_logado:
                contatos[outro_email] = m['remetente_nome']
            elif outro_email not in contatos:
                contatos[outro_email] = "Interessado"

        # 3. LAYOUT DE DUAS COLUNAS (LISTA À ESQUERDA | CHAT À DIREITA)
        col_contatos, col_conversa = st.columns([1.2, 2.5])

        with col_contatos:
            st.markdown("### 👥 Contatos")
            for c_email, c_nome in contatos.items():
                # Container para cada contato com botão de exclusão
                with st.container(border=True):
                    c_btn, c_del = st.columns([4, 1])
                    if c_btn.button(f"👤 {c_nome}\n({c_email})", key=f"btn_{c_email}", use_container_width=True):
                        st.session_state['vrs_chat_ativo'] = c_email
                        st.session_state['vrs_nome_ativo'] = c_nome
                        st.rerun()
                    
                    # BOTÃO DE EXCLUIR CONTATO (LIXEIRA)
                    if c_del.button("🗑️", key=f"del_{c_email}", help=f"Excluir conversa com {c_nome}"):
                        # Deleta todas as mensagens trocadas com este contato
                        for m in lista_geral:
                            if c_email in m['envolvidos']:
                                db.collection("mensagens_chat").document(m['id']).delete()
                        
                        # Se o contato excluído era o ativo, limpa a conversa da tela
                        if st.session_state.get('vrs_chat_ativo') == c_email:
                            st.session_state['vrs_chat_ativo'] = None
                        
                        st.success("Conversa excluída!")
                        st.rerun()

        with col_conversa:
            if 'vrs_chat_ativo' in st.session_state and st.session_state['vrs_chat_ativo']:
                destinatario = st.session_state['vrs_chat_ativo']
                st.markdown(f"#### 🗨️ Conversa com {st.session_state.get('vrs_nome_ativo', destinatario)}")
                
                with st.container(height=450, border=True):
                    for msg in lista_geral:
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

                with st.form("form_resposta_vrs", clear_on_submit=True):
                    c_input, c_send = st.columns([8, 2])
                    msg_txt = c_input.text_input("Sua resposta...", placeholder="Digite aqui...")
                    if c_send.form_submit_button("ENVIAR 🚀", use_container_width=True):
                        if msg_txt:
                            enviar_mensagem_vrs(db, destinatario, msg_txt, "Resposta Direta")
                            st.rerun()
            else:
                st.markdown("<div style='text-align: center; margin-top: 100px; color: #666;'><h3>⬅️ Selecione um contato</h3></div>", unsafe_allow_html=True)

    except Exception as e:
        st.error("🚨 ERRO DE SINCRONIZAÇÃO")
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