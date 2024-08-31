import streamlit as st
from api import get_response
import speech_recognition as sr
import os
from gtts import gTTS
from playsound import playsound
import pygame
pygame.mixer.init()

st.set_page_config(page_title="Supreme Court of India Chatbot", layout="wide")
st.markdown(
    """
<style>
    .st-emotion-cache-janbn0 {
        flex-direction: row-reverse;
        text-align: right;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("SCI Chat \n---------------------------------------------------------------------------------------------")

tts_button = st.toggle("Read Aloud")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    response = "How may I help you?"
    st.session_state.messages.append({"role": "assistant", "content": response,})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        avatar = "👨‍💻"
    elif message["role"] == "assistant":
        avatar = "https://uxdt.nic.in/wp-content/uploads/2020/01/NE_Preview1.png?x38773"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

voice_button = st.empty()

# Voice input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source, timeout=10)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Sorry, I could not request results from the speech recognition service."

#Microphone button for voice input
if voice_button.button("🎤 Speak"):
    voice_input = recognize_speech()
    if voice_input:
        st.session_state.messages.append({"role": "user", "content": voice_input})
        with st.chat_message("user", avatar="👨‍💻"):
            st.markdown(voice_input)
        # Send voice input to the API for processing
        with st.chat_message("assistant", avatar="https://uxdt.nic.in/wp-content/uploads/2020/01/NE_Preview1.png?x38773"):
            response = get_response(user="frontend", prompt=voice_input)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

        if tts_button:
            myobj = gTTS(text=response,slow=False)
            myobj.save("speech.mp3")
            pygame.mixer.music.load("speech.mp3")
            pygame.mixer.music.play()
            pygame.mixer.music.play(0)
            # playsound('speech.mp3')
            # os.system("start speech.mp3")
            # os.system("mpg321 welcome.mp3")   #for linux

        st.rerun()


# Accept text input
if prompt := st.chat_input("Ask Something:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar="https://uxdt.nic.in/wp-content/uploads/2020/01/NE_Preview1.png?x38773"):
        response = get_response(user="frontend", prompt=prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

    if tts_button:
        myobj = gTTS(text=response,slow=False)
        myobj.save("speech.mp3")
        pygame.mixer.music.load("speech.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.play(0)
        # playsound('speech.mp3')
        # os.system("start speech.mp3")
        # os.system("mpg321 welcome.mp3")   #for linux

    st.rerun()

    


