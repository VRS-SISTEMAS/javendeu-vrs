import streamlit as st
import time

def exibir_banner_rotativo_vrs(db, estado_atual="Brasil"):
    """Exibe publicidade com rotação automática simples."""
    try:
        query = db.collection("publicidade").where("estado_alvo", "in", ["Brasil", estado_atual]).stream()
        lista = [b.to_dict() for b in query]
        
        if lista:
            # Muda o banner a cada 10 segundos baseado no relógio
            idx = (int(time.time()) // 10) % len(lista)
            banner = lista[idx]
            
            st.markdown(f"""
                <div style="text-align:center; margin-bottom:20px;">
                    <a href="{banner['link']}" target="_blank">
                        <img src="data:image/jpeg;base64,{banner['foto']}" style="width:100%; border-radius:10px; max-height:250px; object-fit:cover;">
                    </a>
                </div>
            """, unsafe_allow_html=True)
    except:
        pass