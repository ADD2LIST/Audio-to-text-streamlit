import streamlit as st
import pyttsx3
from io import BytesIO
import base64

def text_to_speech(text):
    # Initializing the pyttsx3 engine
    engine = pyttsx3.init()

    # Creating an in-memory file to store the audio
    audio_file = BytesIO()

    # Saving the audio to the in-memory file
    engine.save_to_file(text, audio_file)
    engine.runAndWait()

    # Resetting the in-memory file pointer
    audio_file.seek(0)
    return audio_file

# Streamlit app
def main():
    st.title("Text to Speech Converter")

    # Text input
    text = st.text_area("Enter text:", "Welcome to geeksforgeeks!")

    # Convert button
    if st.button("Convert to Audio"):
        audio_file = text_to_speech(text)

        # Generate audio player
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        st.audio(audio_bytes, format='audio/wav')

        # Download link
        href = f'<a href="data:audio/wav;base64,{audio_base64}" download="audio.wav">Download Audio</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    
    
