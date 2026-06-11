import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi

st.title("Extrair Transcrição do YouTube 🎥")
st.write("Cole o link do vídeo abaixo para baixar o texto.")

url = st.text_input("Link do vídeo:")

if st.button("Gerar Arquivo"):
    if url:
        try:
            # Pega o ID
            if "v=" in url:
                video_id = url.split("v=")[1].split("&")[0]
            elif "youtu.be/" in url:
                video_id = url.split("youtu.be/")[1].split("?")[0]
            else:
                video_id = url
                
            # Baixa e formata
            transcricao = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
            texto_final = "\n".join([linha['text'] for linha in transcricao])
            
            st.success("Sucesso! Clique abaixo para baixar.")
            
            # Botão de download
            st.download_button(
                label="📥 Baixar .txt",
                data=texto_final,
                file_name="transcricao.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"Erro: Verifique o link ou se o vídeo possui legendas ocultas.")