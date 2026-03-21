# =================================================================
# VRS SISTEMAS
# JÁ VENDEU? - MÓDULO: principal.py (VERSÃO SEGURANÇA MÁXIMA)
# FUNÇÕES: VITRINE, DETALHES, DENÚNCIAS E AVALIAÇÕES
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import importlib
import base64
import datetime

st.set_page_config(page_title="JÁ VENDEU? - Marketplace VRS", layout="wide", initial_sidebar_state="expanded")

import conexao
import interface_javendeu_vrs
import usuarios_vrs
import anuncios_vrs
import categorias
import chat 

# Garante que as atualizações de segurança sejam carregadas
importlib.reload(usuarios_vrs)
importlib.reload(anuncios_vrs)
importlib.reload(chat)

interface_javendeu_vrs.aplicar_estilo_vrs()
db = conexao.conectar_banco_vrs()

# CSS MESTRE PARA TRAVAR O TAMANHO DAS FOTOS E ESTILIZAR COMENTÁRIOS
st.markdown("""
    <style>
    .moldura-foto-vrs {
        background-color: #0E1117;
        border: 1px solid #333;
        border-radius: 10px;
        height: 400px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }
    .moldura-foto-vrs img {
        max-height: 400px;
        max-width: 100%;
        object-fit: contain;
    }
    .caixa-comentario {
        background-color: #1A1C24;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #FF4B4B;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

if 'pagina_vrs' not in st.session_state: st.session_state['pagina_vrs'] = "Home"
if 'anuncio_detalhe' not in st.session_state: st.session_state['anuncio_detalhe'] = None

col_vazia, col_login = st.columns([8, 2])
with col_login:
    if db is not None:
        usuarios_vrs.gerenciar_acesso(db)

interface_javendeu_vrs.obter_menu_lateral_vrs()

# --- LÓGICA DE DETALHES DO PRODUTO (ONDE AS TRAVAS ATUAM) ---
if st.session_state['anuncio_detalhe']:
    item = st.session_state['anuncio_detalhe']
    
    # 🛡️ TRAVA 1: EXIBIR ALERTA DE SEGURANÇA NO TOPO
    anuncios_vrs.exibir_alerta_seguranca_vrs()
    
    st.markdown(f"## {item.get('titulo', 'Produto')}")
    
    col_img, col_info = st.columns([1.5, 1])
    
    with col_img:
        fotos = item.get('fotos', [])
        if not fotos and 'foto' in item: fotos = [item['foto']]
        if fotos:
            titulos_fotos = [f"FOTO {i+1}" for i in range(len(fotos))]
            tabs_carrossel = st.tabs(titulos_fotos)
            for i, f_b64 in enumerate(fotos):
                with tabs_carrossel[i]:
                    st.markdown(f'<div class="moldura-foto-vrs"><img src="data:image/jpeg;base64,{f_b64}"></div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Sem fotos disponíveis.")

    with col_info:
        with st.container(border=True):
            st.markdown(f"<h1 style='color: #FF4B4B; margin:0;'>R$ {item.get('preco', 0.0):.2f}</h1>", unsafe_allow_html=True)
            st.markdown(f"📍 **{item.get('cidade', 'N/A')} - {item.get('estado', 'N/A')}**")
            st.markdown(f"**📁 Categoria:** {item.get('categoria', 'Geral')}")
            st.markdown(f"👤 **Vendedor:** {item.get('vendedor_nome', 'Usuário VRS')}")
            st.markdown("---")
            st.write("**Descrição:**")
            st.write(item.get('descricao', 'Sem descrição.'))
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- BOTÕES DE INTERAÇÃO SEGUROS ---
            col_b1, col_b2 = st.columns(2)
            
            if col_b1.button("💬 CHAT INTERNO", use_container_width=True, type="primary"):
                if st.session_state.get('logado'):
                    st.session_state['vrs_chat_ativo'] = item['vendedor_email']
                    st.session_state['vrs_produto_atual'] = item['titulo']
                    chat.enviar_mensagem_vrs(db, item['vendedor_email'], f"Olá! Vi seu anúncio '{item['titulo']}' e tenho interesse.", item['titulo'])
                    st.session_state['pagina_vrs'] = "Chat"
                    st.session_state['anuncio_detalhe'] = None
                    st.rerun()
                else:
                    st.error("⚠️ Faça login para usar o chat.")

            # Botão de WhatsApp (Se houver número cadastrado)
            zap_vendedor = item.get('vendedor_whatsapp', '')
            if zap_vendedor:
                link_zap = f"https://wa.me/55{zap_vendedor}?text=Olá! Vi seu anúncio '{item['titulo']}' no site Já Vendeu? e tenho interesse."
                col_b2.link_button("🟢 WHATSAPP", link_zap, use_container_width=True)

            st.markdown("---")
            
            # 🛡️ TRAVA 2: BOTÃO DE DENÚNCIA
            if st.button("🚩 DENUNCIAR ESTE ANÚNCIO", use_container_width=True):
                anuncios_vrs.registrar_denuncia_vrs(db, item.get('id', 'N/A'), item.get('titulo', 'N/A'))
                st.warning("Denúncia enviada para a central VRS Soluções.")

            if st.button("⬅️ VOLTAR PARA A VITRINE", use_container_width=True):
                st.session_state['anuncio_detalhe'] = None
                st.rerun()

    # --- SEÇÃO DE AVALIAÇÕES E COMENTÁRIOS (SUGESTÃO DO VITOR) ---
    st.markdown("---")
    st.subheader("⭐ Avaliações do Vendedor")
    
    col_av1, col_av2 = st.columns([2, 1])
    
    with col_av1:
        # Busca avaliações no Firebase
        id_anuncio = item.get('id', 'N/A')
        comentarios = db.collection("avaliacoes").where("vendedor_email", "==", item['vendedor_email']).stream()
        tem_comentario = False
        for c in comentarios:
            tem_comentario = True
            dados_c = c.to_dict()
            st.markdown(f"""
                <div class="caixa-comentario">
                    <b>{dados_c['nome_avaliador']}</b> - Nota: {'⭐' * int(dados_c['nota'])}<br>
                    <small>{dados_c['data']}</small><br>
                    {dados_c['texto']}
                </div>
            """, unsafe_allow_html=True)
        if not tem_comentario:
            st.info("Este vendedor ainda não recebeu avaliações. Seja o primeiro!")

    with col_av2:
        if st.session_state.get('logado'):
            with st.form("form_avaliar_vrs"):
                st.write("Deixe sua avaliação:")
                nota = st.slider("Nota", 1, 5, 5)
                coment_txt = st.text_area("Comentário", placeholder="Como foi sua experiência?")
                if st.form_submit_button("ENVIAR AVALIAÇÃO"):
                    if coment_txt:
                        db.collection("avaliacoes").add({
                            "vendedor_email": item['vendedor_email'],
                            "nome_avaliador": st.session_state['usuario']['nome'],
                            "nota": nota,
                            "texto": coment_txt,
                            "data": datetime.datetime.now().strftime("%d/%m/%Y")
                        })
                        st.success("Obrigado pela avaliação!")
                        st.rerun()
        else:
            st.caption("Faça login para avaliar este vendedor.")

# --- LÓGICA DA HOME / VITRINE ---
else:
    pag = st.session_state['pagina_vrs']
    if pag == "Home":
        interface_javendeu_vrs.exibir_identidade_visual_vrs()
        interface_javendeu_vrs.exibir_conversor_vrs()
        st.markdown("---")
        
        st.subheader("🛍️ Vitrine de Ofertas")
        f_col1, f_col2, f_col3 = st.columns([2, 1, 2])
        
        cat_filtro = f_col1.selectbox("O que você procura?", ["Todas"] + categorias.obter_categorias_vrs())
        est_filtro = f_col2.selectbox("Estado", ["Brasil"] + anuncios_vrs.ESTADOS_BR)
        cid_filtro = f_col3.text_input("Cidade (opcional)", placeholder="Ex: Duque de Caxias").strip().title()

        try:
            if db:
                query = db.collection("anuncios").where("status", "==", "ativo")
                docs = query.stream()
                lista_anuncios = []
                
                for d in docs:
                    it = d.to_dict()
                    match_cat = (cat_filtro == "Todas" or it.get('categoria') == cat_filtro)
                    match_est = (est_filtro == "Brasil" or it.get('estado') == est_filtro)
                    match_cid = (not cid_filtro or cid_filtro in it.get('cidade', ''))
                    
                    if match_cat and match_est and match_cid:
                        lista_anuncios.append(it | {"id": d.id})

                if not lista_anuncios:
                    st.warning("🧐 Nenhuma oferta encontrada para os filtros selecionados.")
                else:
                    cols_vitrine = st.columns(4)
                    for idx, anuncio in enumerate(lista_anuncios):
                        with cols_vitrine[idx % 4]:
                            with st.container(border=True):
                                f_capa = anuncio['fotos'][0] if 'fotos' in anuncio and anuncio['fotos'] else anuncio.get('foto', "")
                                if f_capa: 
                                    st.image(f"data:image/jpeg;base64,{f_capa}", use_container_width=True)
                                st.markdown(f"**{anuncio.get('titulo', 'Sem Título')}**")
                                st.markdown(f"<h4 style='color: #FF4B4B;'>R$ {anuncio.get('preco', 0.0):.2f}</h4>", unsafe_allow_html=True)
                                st.caption(f"📍 {anuncio.get('cidade', 'N/A')}")
                                if st.button("Ver Detalhes", key=f"vit_{anuncio['id']}", use_container_width=True):
                                    st.session_state['anuncio_detalhe'] = anuncio
                                    st.rerun()
        except Exception as e:
            st.error(f"Erro na vitrine: {e}")
            
    elif pag in ["Anunciar", "Meus Anúncios"]:
        anuncios_vrs.exibir_painel_vendedor(db)
    elif pag == "Chat":
        chat.exibir_interface_chat(db)

    interface_javendeu_vrs.exibir_rodape_vrs()