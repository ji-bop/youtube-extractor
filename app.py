import re
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi

def extrair_id_video(url: str) -> str:
    """Extrai o ID do vídeo a partir de qualquer URL do YouTube."""
    url = url.strip()
    # Padrão seguro para identificar o ID de 11 caracteres do YouTube
    padrao = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(padrao, url)
    
    return match.group(1) if match else url

def buscar_transcricao(video_id: str) -> str:
    """Busca e une as linhas da transcrição em um único texto."""
    transcricao = YouTubeTranscriptApi().fetch(video_id, languages=['pt', 'pt-BR', 'en'])
    return "\n".join([linha.text for linha in transcricao])

def main():
    """Função principal que constrói a interface web."""
    st.title("Extrair Transcrição do YouTube 🎥")
    st.write("Cole o link do vídeo abaixo para baixar o texto.")

    url = st.text_input("Link do vídeo:")

    if st.button("Gerar Arquivo") and url:
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
            st.error(f"Erro ao processar o vídeo. Detalhe: {e}")

# Executa o aplicativo
if __name__ == "__main__":
    main()
