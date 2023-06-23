import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64

def text_to_speech(text, language):
    # Creating the audio file using gTTS
    tts = gTTS(text=text, lang=language, slow=False)
    audio_file = BytesIO()
    tts.save(audio_file)
    audio_file.seek(0)
    return audio_file

# Streamlit app
def main():
    st.title("Text to Speech Converter")

    # Text input
    text = st.text_area("Enter text:", "Welcome to geeksforgeeks!")

    # Language selection
    language = st.selectbox("Select language:", ("en", "fr", "es"))  # Add more languages if needed

    # Convert button
    if st.button("Convert to Audio"):
        audio_file = text_to_speech(text, language)

        # Generate audio player
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        st.audio(audio_bytes, format='audio/mp3')

        # Download link
        href = f'<a href="data:audio/mp3;base64,{audio_base64}" download="audio.mp3">Download Audio</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
  
