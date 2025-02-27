

import streamlit as st
from datetime import datetime
from agents_1 import ConversationalAgent, ValidationAgent, HypnosisScriptGenerator
from src.models import ChatMessage
import speech_recognition as sr
from typing import Optional
import time
from openai import OpenAI
import io
import wave
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play

st.set_page_config(
    page_title="AI Hypnosis Consultation",
    layout="centered",
)
# Constants
CURRENT_TIME = "2025-02-03 14:56:58"
CURRENT_USER = "🧘"
MAX_QUESTIONS = 4  # Maximum number of questions before generating the script
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

def scriptvoice(script):
    client_11lab = ElevenLabs(api_key=st.secrets['ELEVENLABS_API_KEY'])
    audio = client_11lab.text_to_speech.convert(
    text=script,
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
    )
    return audio

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversation_agent' not in st.session_state:
        st.session_state.conversation_agent = None
    if 'validation_agent' not in st.session_state:
        st.session_state.validation_agent = ValidationAgent()
    if 'script_generator' not in st.session_state:
        st.session_state.script_generator = None
    if 'script_generated' not in st.session_state:
        st.session_state.script_generated = False
    if 'last_audio' not in st.session_state:
        st.session_state.last_audio = None
    if 'question_count' not in st.session_state:  # Add question counter
        st.session_state.question_count = 0

def display_chat_message(message):
    with st.chat_message(message["role"], avatar="🧘" if message["role"] == "assistant" else "👤"):
        st.write(message["content"])

def handle_user_input(user_input: str):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get conversation agent's response
    with st.spinner("Thinking..."):
        response = st.session_state.conversation_agent.get_next_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Increment question counter
    st.session_state.question_count += 1
    print(f"Question count: {st.session_state.question_count}")
    
    # Check if all questions are answered
    if not st.session_state.script_generated:
        conversation_history = st.session_state.conversation_agent.get_conversation_history()
        is_complete = st.session_state.validation_agent.validate_conversation(conversation_history)
        
        # Force completion after MAX_QUESTIONS
        if is_complete or st.session_state.question_count >= MAX_QUESTIONS:
            # Notify user if we're forcing completion based on question count
            if not is_complete and st.session_state.question_count >= MAX_QUESTIONS:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Thanks for sharing your experiences with me. I've gathered enough information to create a personalized hypnosis script for you."
                })
            
            with st.spinner("Generating your personalized hypnosis script..."):
                script = st.session_state.script_generator.generate_script(
                    conversation_history=conversation_history
                )
                st.session_state.script_generated = True
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Here's your personalized hypnosis script:"
                })
                st.session_state.messages.append({"role": "assistant", "content": script})
                
                # Generate audio for the script
                try:
                    audio = scriptvoice(script)
                    audio_buffer = io.BytesIO(audio)
                    st.session_state.messages.append({"role": "assistant", "content": "Listen to your hypnosis session:"})
                    st.session_state.messages.append({"role": "assistant", "content": st.audio(audio_buffer, format="audio/mp3")})
                except Exception as e:
                    st.session_state.messages.append({"role": "assistant", "content": f"Audio generation failed: {str(e)}"})

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

def convert_audio_bytes_to_audio_data(audio_bytes):
    """
    Converts raw WAV audio bytes into a speech_recognition.AudioData object.
    """
    # Create an in-memory stream from the audio bytes
    audio_stream = io.BytesIO(audio_bytes)
    with wave.open(audio_stream, "rb") as wf:
        sample_rate = wf.getframerate()
        sample_width = wf.getsampwidth()
        frame_data = wf.readframes(wf.getnframes())
    return sr.AudioData(frame_data, sample_rate, sample_width)

def main():
    st.title("AI Hypnosis Consultation")

    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        selected_model = st.selectbox("Select a model", ["openai", "anthropic", "deepseek"])
        if selected_model == "openai":
            st.session_state.conversation_agent = ConversationalAgent(llm_name="openai")
            st.session_state.script_generator = HypnosisScriptGenerator(llm_name="openai")
           
        elif selected_model == "anthropic":
            st.session_state.conversation_agent = ConversationalAgent(llm_name="anthropic")
            st.session_state.script_generator = HypnosisScriptGenerator(llm_name="anthropic")
          
        elif selected_model == "deepseek":
            st.session_state.conversation_agent = ConversationalAgent(llm_name="deepseek")
            st.session_state.script_generator = HypnosisScriptGenerator(llm_name="deepseek")
           
        st.write(f"Current User: {CURRENT_USER}")
        st.write(f"Current Time (UTC): {CURRENT_TIME}")
        
        if st.button("Start New Chat"):
            st.session_state.messages = []
            st.session_state.script_generated = False
            st.session_state.conversation_agent = None
            st.session_state.last_audio = None
            st.session_state.question_count = 0  # Reset question counter
            st.rerun()
        
        # Display question counter and progress
        st.progress(min(st.session_state.question_count / MAX_QUESTIONS, 1.0))
        st.write(f"Questions: {st.session_state.question_count}/{MAX_QUESTIONS}")
        
        input_method = st.radio(
            "Choose Input Method",
            ["Text", "Voice"],
            key="input_method"
        )

        if input_method == "Voice":
            st.markdown("""
            ### Voice Input Instructions:
            1. Click the microphone icon to start recording
            2. Speak clearly into your microphone
            3. Wait for the transcript to appear
            4. Your message will be automatically sent
            """)

    # Display chat messages
    for message in st.session_state.messages:
        display_chat_message(message)

    # Initialize chat with welcome message if empty
    if not st.session_state.messages and st.session_state.conversation_agent is not None:
        initial_response = st.session_state.conversation_agent.get_next_response()
        st.session_state.messages.append({"role": "assistant", "content": initial_response})
        st.rerun()

    # Input handling
    if input_method == "Voice":
        audio_bytes = st.audio_input("Record your message")
        if audio_bytes is not None and audio_bytes != st.session_state.last_audio:
            st.session_state.last_audio = audio_bytes
            
            with st.spinner("Processing your voice input..."):
                try:
                    audio_byte = audio_bytes.read()
                    audio_data = convert_audio_bytes_to_audio_data(audio_byte)
                    transcript = sr.Recognizer().recognize_google(audio_data)
                    if transcript:
                        # Show transcript
                        st.info(f"You said: {transcript}")
                        # Process the input
                        handle_user_input(transcript)
                        
                        st.rerun()
                        audio_bytes = None
                    
                except sr.UnknownValueError:
                    st.error("Could not understand the audio. Please try again.")
                   
                except sr.RequestError:
                    st.error("Could not request results from speech recognition service")
                   
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                
    else:  # Text input
        if prompt := st.chat_input("Type your response here..."):
            handle_user_input(prompt)
            st.rerun()

# if _name_ == "_main_":
main()