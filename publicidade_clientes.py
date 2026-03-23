# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: publicidade_clientes.py (GESTÃO DE BANNERS - VERSÃO FINAL)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime

def gerenciar_banners_vrs(db):
    """Interface para o Vitor cadastrar e remover banners no painel ADM."""
    st.subheader("🚀 Gestão de Banners Publicitários")
    
    with st.expander("➕ Cadastrar Novo Banner", expanded=False):
        with st.form("form_novo_banner", clear_on_submit=True):
            cliente = st.text_input("Nome do Cliente/Empresa*")
            link = st.text_input("Link de Destino (WhatsApp ou Site)*", placeholder="https://wa.me/55...")
            
            col1, col2 = st.columns(2)
            ESTADOS = ["Brasil", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
            uf = col1.selectbox("Onde exibir este banner?", ESTADOS)
            vencimento = col2.date_input("Data de Vencimento")
            
            arq_banner = st.file_uploader("Imagem do Banner (Recomendado: 1200x200px)", type=['png', 'jpg', 'jpeg'])
            
            if st.form_submit_button("✅ ATIVAR PUBLICIDADE", use_container_width=True):
                if cliente and link and arq_banner:
                    img_b64 = base64.b64encode(arq_banner.getvalue()).decode('utf-8')
                    
                    dados_banner = {
                        "cliente": cliente,
                        "link": link,
                        "estado_alvo": uf,
                        "vencimento": str(vencimento),
                        "foto": img_b64,
                        "cliques": 0,
                        "data_criacao": datetime.datetime.now()
                    }
                    
                    db.collection("publicidade").add(dados_banner)
                    st.success(f"Banner de {cliente} está no ar!")
                    st.rerun()
                else:
                    st.error("Preencha todos os campos corretamente.")

    st.markdown("---")
    st.write("### Banners Ativos")
    
    try:
        banners = db.collection("publicidade").stream()
        for b in banners:
            d = b.to_dict()
            with st.container(border=True):
                c1, c2, c3 = st.columns([2, 3, 1])
                with c1:
                    st.image(f"data:image/jpeg;base64,{d['foto']}", use_container_width=True)
                with c2:
                    st.markdown(f"**Cliente:** {d['cliente']}")
                    st.caption(f"Exibindo em: {d['estado_alvo']} | Vence em: {d['vencimento']}")
                with c3:
                    if st.button("🗑️ Parar", key=f"del_ban_{b.id}", use_container_width=True):
                        db.collection("publicidade").document(b.id).delete()
                        st.rerun()
    except:
        st.info("Nenhum banner cadastrado ainda.")

def exibir_banner_rotativo_vrs(db, estado_atual="Brasil"):
    """Exibe o banner na Home baseado no filtro de estado (LÓGICA FLEXÍVEL)."""
    try:
        # Busca banners 'Brasil' OU o estado selecionado pelo usuário
        filtros_busca = ["Brasil"]
        if estado_atual != "Brasil":
            filtros_busca.append(estado_atual)

        query = db.collection("publicidade").where("estado_alvo", "in", filtros_busca).stream()
        lista_banners = [b.to_dict() | {"id": b.id} for b in query]
        
        if lista_banners:
            # Pega o último banner ativo para exibição
            banner = lista_banners[-1] 
            
            html_banner = f"""
                <a href="{banner['link']}" target="_blank" style="text-decoration: none;">
                    <div style="width: 100%; border-radius: 10px; overflow: hidden; border: 1px solid #333; margin-bottom: 20px; box-shadow: 0px 4px 15px rgba(0,0,0,0.5);">
                        <img src="data:image/jpeg;base64,{banner['foto']}" style="width: 100%; display: block;">
                    </div>
                </a>
            """
            st.markdown(html_banner, unsafe_allow_html=True)
    except:
        pass