import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64
from pydub import AudioSegment
import tempfile
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode

class AudioPlayerProcessor(AudioProcessorBase):
    def recv(self, frame):
        st.audio(frame.to_ndarray(), format='audio/mp3')

def text_to_speech(text, language):
    # Creating the audio file using gTTS
    tts = gTTS(text=text, lang=language, slow=False)
    audio_file = BytesIO()
    tts.save(audio_file)
    audio_file.seek(0)
    return audio_file

def convert_to_wav(audio_bytes):
    # Load audio file and convert to WAV format
    audio = AudioSegment.from_file(audio_bytes, format="mp3")
    wav_file = BytesIO()
    audio.export(wav_file, format="wav")
    wav_file.seek(0)
    return wav_file

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

        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(audio_bytes)
            temp.flush()

            webrtc_streamer(
                key="audio-player",
                mode=WebRtcMode.SEND_RECEIVE,
                audio_processor_factory=AudioPlayerProcessor,
                filename=temp.name,
                mimeType="audio/mp3",
            )

        # Convert to WAV and provide download link
        wav_file = convert_to_wav(audio_file)
        wav_bytes = wav_file.read()
        wav_base64 = base64.b64encode(wav_bytes).decode('utf-8')
        href = f'<a href="data:audio/wav;base64,{wav_base64}" download="audio.wav">Download Audio</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    
