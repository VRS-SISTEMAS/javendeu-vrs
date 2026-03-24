# =================================================================
# VRS SOLUÇÕES - JÁ VENDEU?
# MÓDULO: publicidade_clientes.py (REDIMENSIONAMENTO AUTOMÁTICO - ANTI-ERRO 400)
# DESENVOLVIDO POR: Iara (Gemini) para Vitor
# =================================================================
import streamlit as st
import base64
import datetime
import io  # Biblioteca para lidar com streams de dados (para imagem)

# Importa a biblioteca Pillow (PIL) para redimensionar a imagem
try:
    from PIL import Image
except ImportError:
    st.error("🚨 Erro: A biblioteca 'Pillow' não está instalada. Execute 'pip install Pillow' no terminal.")
    st.stop()

def gerenciar_banners_vrs(db):
    """Painel administrativo para o Vitor cadastrar publicidade paga."""
    st.subheader("🚀 Gestão de Banners")
    
    # Formulário para novo banner
    with st.expander("➕ Novo Banner de Cliente", expanded=True):
        cliente = st.text_input("Nome do Cliente", key="vrs_pub_nome")
        link = st.text_input("Link WhatsApp/Site (com https://)", key="vrs_pub_link")
        # Opção 'Brasil' é a padrão para alcance nacional
        uf = st.selectbox("Estado Alvo", ["Brasil", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"], key="vrs_pub_uf")
        arq = st.file_uploader("Upload do Banner", type=['png', 'jpg', 'jpeg'], key="vrs_pub_img")
        
        enviar = st.button("✅ ATIVAR PUBLICIDADE", use_container_width=True)
        
        if enviar:
            if cliente and link and arq:
                try:
                    # 1. PROCESSAMENTO E REDIMENSIONAMENTO AUTOMÁTICO (SOLUÇÃO PARA O ERRO 400)
                    
                    # Abre a imagem original usando a biblioteca Pillow
                    img_original = Image.open(arq)
                    
                    # Converte para RGB (garante compatibilidade com JPEG)
                    if img_original.mode in ('RGBA', 'LA', 'P'):
                        img_original = img_original.convert('RGB')
                    
                    # Define o tamanho ideal para o banner da VRS (Ex: 1200x200px)
                    # Você pode ajustar esses números conforme o design desejado
                    tamanho_ideal = (1200, 200) 
                    
                    # Redimensiona a imagem usando um filtro de alta qualidade
                    img_redimensionada = img_original.resize(tamanho_ideal, Image.Resampling.LANCZOS)
                    
                    # 2. CONVERSÃO PARA BASE64 E COMPRESSÃO
                    
                    # Cria um buffer de memória para salvar a imagem processada
                    buffer = io.BytesIO()
                    
                    # Salva a imagem redimensionada no buffer como JPEG compactado (qualidade 80)
                    # Isso reduz drasticamente o tamanho do arquivo
                    img_redimensionada.save(buffer, format="JPEG", quality=80)
                    
                    # Pega os bytes da imagem compactada
                    img_data = buffer.getvalue()
                    
                    # Verifica se o tamanho final ficou dentro do limite do Firebase (1MB)
                    tamanho_final_kb = len(img_data) / 1024
                    if tamanho_final_kb > 900: # Deixa uma margem de segurança de 100KB
                        st.error(f"❌ Erro: Mesmo redimensionada, a imagem ficou com {tamanho_final_kb:.1f}KB. Tente uma imagem original mais leve.")
                        return

                    # Converte para Base64 para gravar no banco
                    img_b64 = base64.b64encode(img_data).decode('utf-8')
                    
                    # 3. GRAVAÇÃO NO BANCO VRS
                    db.collection("publicidade").add({
                        "cliente": cliente, 
                        "link": link, 
                        "estado_alvo": uf,
                        "foto": img_b64, 
                        "data_cadastro": datetime.datetime.now()
                    })
                    st.success(f"✅ Banner de '{cliente}' ativado com sucesso! (Tamanho final: {tamanho_final_kb:.1f}KB)")
                    st.rerun() # Atualiza a página para mostrar o novo banner e atualizar o contador

                except Exception as e:
                    st.error(f"❌ Erro ao processar ou gravar: {e}")
            else:
                st.warning("⚠️ Preencha todos os campos obrigatórios e selecione uma imagem.")

    st.markdown("---")
    st.subheader("📋 Banners Ativos")
    
    # Listagem para remoção
    try:
        banners = db.collection("publicidade").order_by("data_cadastro", direction="DESCENDING").stream()
        tem_banner = False
        for b in banners:
            tem_banner = True
            d = b.to_dict()
            with st.container(border=True):
                col_img, col_txt = st.columns([1, 2])
                with col_img:
                    st.image(f"data:image/jpeg;base64,{d['foto']}", use_container_width=True)
                with col_txt:
                    st.write(f"**Cliente:** {d['cliente']}")
                    st.write(f"**Alvo:** {d['estado_alvo']}")
                    if st.button("🗑️ Remover Banner", key=f"del_pub_{b.id}"):
                        db.collection("publicidade").document(b.id).delete()
                        st.rerun()
        if not tem_banner:
            st.info("Nenhum banner cadastrado no momento.")
    except Exception as e:
        pass

def exibir_banner_rotativo_vrs(db, estado_atual="Brasil"):
    """
    Exibe o banner nacional no topo da vitrine. 
    LÓGICA NACIONAL: Busca banners marcados como 'Brasil' para alcance nacional.
    """
    try:
        # Busca banners com alvo 'Brasil' (Independente do filtro regional do usuário)
        query = db.collection("publicidade").where("estado_alvo", "==", "Brasil").stream()
        lista_banners = [b.to_dict() for b in query]
        
        if lista_banners:
            # Exibe o banner mais recente (o último da lista)
            banner = lista_banners[-1]
            
            # HTML para exibição na interface
            st.markdown(f"""
                <div style="width:100%; margin-top: 10px; margin-bottom: 20px;">
                    <a href="{banner['link']}" target="_blank">
                        <img src="data:image/jpeg;base64,{banner['foto']}" 
                             style="width:100%; border-radius:10px; border: 1px solid #333; box-shadow: 0px 4px 12px rgba(0,0,0,0.4);">
                    </a>
                </div>
            """, unsafe_allow_html=True)
    except Exception:
        pass # Falha silenciosa para não quebrar a Home