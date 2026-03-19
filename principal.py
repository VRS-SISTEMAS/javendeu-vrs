# =================================================================
# VRS Soluções - JÁ VENDEU? - MÓDULO: principal.py
# FUNÇÕES: VITRINE, NAVEGAÇÃO E INTEGRAÇÃO COM CHAT WHATSAPP
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import importlib

# REGRA DE OURO: O set_page_config deve ser a primeira instrução Streamlit
st.set_page_config(page_title="JÁ VENDEU? - Marketplace VRS", layout="wide", initial_sidebar_state="expanded")

# Importação dos módulos do sistema
import conexao
import interface_javendeu_vrs
import usuarios_vrs
import anuncios_vrs
import categorias
import chat 

# --- SOLUÇÃO PARA O ERRO ATTRIBUTEERROR ---
# Forçamos o Python a recarregar os módulos para garantir que ele veja as funções novas
importlib.reload(usuarios_vrs)
importlib.reload(chat)

# 1. Configurações Visuais e Conexão com Banco de Dados
interface_javendeu_vrs.aplicar_estilo_vrs()
db = conexao.conectar_banco_vrs()

# 2. Inicialização de Estados de Sessão (Persistence)
if 'pagina_vrs' not in st.session_state: st.session_state['pagina_vrs'] = "Home"
if 'anuncio_detalhe' not in st.session_state: st.session_state['anuncio_detalhe'] = None
if 'filtro_categoria' not in st.session_state: st.session_state['filtro_categoria'] = "Todas"

# --- HEADER DE ACESSO (TOPO DIREITO) ---
col_vazia, col_login = st.columns([8, 2])
with col_login:
    # Verificamos se o db existe antes de gerenciar o acesso para evitar bugs
    if db is not None:
        try:
            usuarios_vrs.gerenciar_acesso(db)
        except AttributeError:
            st.error("Erro ao carregar módulo de login. Reinicie o Streamlit.")
    else:
        st.error("Erro Firebase")

# --- MENU LATERAL ---
interface_javendeu_vrs.obter_menu_lateral_vrs()

# --- LÓGICA DE NAVEGAÇÃO PRINCIPAL ---

if st.session_state['anuncio_detalhe']:
    # TELA DE DETALHES DO PRODUTO SELECIONADO
    item = st.session_state['anuncio_detalhe']
    st.markdown(f"## {item['titulo']}")
    
    col_img, col_info = st.columns([1, 1])
    with col_img:
        if "foto" in item and item['foto']:
            st.image(f"data:image/jpeg;base64,{item['foto']}", use_container_width=True)
    with col_info:
        st.subheader(f"💰 R$ {item['preco']:.2f}")
        st.info(f"📁 Categoria: {item.get('categoria', 'Geral')}")
        st.write(f"📝 {item.get('descricao', 'Sem descrição.')}")
        st.markdown("---")
        
        # --- BOTÃO DE INTERAÇÃO COM CHAT ---
        if st.button("💬 TENHO INTERESSE / ABRIR CHAT", use_container_width=True, type="primary"):
            if st.session_state.get('logado'):
                st.session_state['vrs_chat_ativo'] = item['vendedor_email']
                st.session_state['vrs_produto_atual'] = item['titulo']
                
                # Inicia a conversa com mensagem automática
                chat.enviar_mensagem_vrs(db, item['vendedor_email'], f"Olá! Vi seu anúncio '{item['titulo']}' e tenho interesse.", item['titulo'])
                
                st.session_state['pagina_vrs'] = "Chat"
                st.session_state['anuncio_detalhe'] = None
                st.rerun()
            else:
                st.error("⚠️ Faça login para conversar com o vendedor.")

        if st.button("⬅️ VOLTAR PARA A VITRINE", use_container_width=True):
            st.session_state['anuncio_detalhe'] = None
            st.rerun()

else:
    pag = st.session_state['pagina_vrs']
    
    if pag == "Home":
        interface_javendeu_vrs.exibir_identidade_visual_vrs()
        interface_javendeu_vrs.exibir_conversor_vrs()
        st.markdown("---")
        st.subheader("🛍️ Vitrine de Ofertas")
        
        cat_filtro = st.selectbox("O que você procura?", ["Todas"] + categorias.obter_categorias_vrs())
        
        try:
            if db:
                query = db.collection("anuncios").where("status", "==", "ativo")
                if cat_filtro != "Todas":
                    query = query.where("categoria", "==", cat_filtro)
                
                docs = query.stream()
                lista_anuncios = []
                for d in docs:
                    dados = d.to_dict()
                    dados['id'] = d.id
                    lista_anuncios.append(dados)

                if not lista_anuncios:
                    st.warning("🧐 Nenhuma oferta encontrada no momento.")
                else:
                    cols_vitrine = st.columns(4)
                    for idx, anuncio in enumerate(lista_anuncios):
                        with cols_vitrine[idx % 4]:
                            with st.container(border=True):
                                if "foto" in anuncio and anuncio['foto']:
                                    st.image(f"data:image/jpeg;base64,{anuncio['foto']}", use_container_width=True)
                                st.markdown(f"**{anuncio['titulo']}**")
                                st.markdown(f"<h4 style='color: #FF4B4B;'>R$ {anuncio['preco']:.2f}</h4>", unsafe_allow_html=True)
                                if st.button("Ver Detalhes", key=f"vit_{anuncio['id']}", use_container_width=True):
                                    st.session_state['anuncio_detalhe'] = anuncio
                                    st.rerun()
        except Exception as e:
            st.error(f"Erro ao carregar vitrine: {e}")

    elif pag in ["Anunciar", "Meus Anúncios"]:
        anuncios_vrs.exibir_painel_vendedor(db)

    elif pag == "Chat":
        chat.exibir_interface_chat(db)

# Rodapé padrão VRS Soluções
interface_javendeu_vrs.exibir_rodape_vrs()