import re
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

# Lendo as credenciais de forma segura do cofre do Streamlit
WEBSHARE_USERNAME = st.secrets["WEBSHARE_USERNAME"]
WEBSHARE_PASSWORD = st.secrets["WEBSHARE_PASSWORD"]

def extrair_id_video(url: str) -> str:
    """Extrai o ID do vídeo a partir de qualquer URL do YouTube."""
    url = url.strip()
    padrao = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(padrao, url)
    return match.group(1) if match else url

def buscar_transcricao(video_id: str) -> str:
    """Busca a transcrição utilizando o proxy residencial rotativo do Webshare."""
    config_proxy = WebshareProxyConfig(
        proxy_username=WEBSHARE_USERNAME,
        proxy_password=WEBSHARE_PASSWORD
    )
    
    api = YouTubeTranscriptApi(proxy_config=config_proxy)
    transcricao = api.fetch(video_id, languages=['pt', 'pt-BR', 'en'])
    
    return "\n".join([linha.text for linha in transcricao])

def main():
    st.title("Extrair Transcrição do YouTube 🎥")
    st.write("Cole o link do vídeo abaixo para baixar o texto.")

    url = st.text_input("Link do vídeo:")

    if st.button("Gerar Arquivo") and url:
        with st.spinner("Conectando de forma segura e extraindo o texto..."):
            try:
                video_id = extrair_id_video(url)
                texto_final = buscar_transcricao(video_id)
                
                st.success("Sucesso! Clique abaixo para baixar.")
                st.download_button(
                    label="📥 Baixar .txt",
                    data=texto_final,
                    file_name="transcricao.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Erro ao processar o vídeo: {e}")

if __name__ == "__main__":
    main()
