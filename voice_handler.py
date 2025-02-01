# voice_handler.py
import speech_recognition as sr
import streamlit as st
from typing import Optional

class VoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def record_audio(self) -> Optional[str]:
        """Record audio from microphone and return the transcript"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)  # 5 seconds timeout
                
                try:
                    transcript = self.recognizer.recognize_google(audio)
                    return transcript
                except sr.UnknownValueError:
                    st.error("Could not understand the audio. Please try again.")
                    return None
                except sr.RequestError:
                    st.error("Could not request results from speech recognition service")
                    return None
        except Exception as e:
            st.error(f"Error accessing microphone: {str(e)}")
            return None