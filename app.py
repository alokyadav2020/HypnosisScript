# # main.py
# import streamlit as st
# from datetime import datetime
# from agents import ConversationalAgent, ValidationAgent, HypnosisScriptGenerator
# from models import ChatMessage
# import speech_recognition as sr
# from typing import Optional


# # Constants
# CURRENT_TIME = "2025-02-01 14:37:21"
# CURRENT_USER = "🧘"

# class VoiceHandler:
#     def __init__(self):
#         self.recognizer = sr.Recognizer()
#         self.microphone = sr.Microphone()
#         # self.audio_input = st.audio_input("Record your voice here")
        
#     def record_audio(self) -> Optional[str]:
#         """Record audio from microphone and return the transcript"""
#         try:
#             with self.microphone as source:
#                 self.recognizer.adjust_for_ambient_noise(source)
#                 audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)  # 5 seconds timeout

#                 # audio= st.audio_input("Record your voice here")
                
#                 try:
#                     transcript = self.recognizer.recognize_google(audio)
#                     return transcript
#                 except sr.UnknownValueError:
#                     st.error("Could not understand the audio. Please try again.")
#                     return None
#                 except sr.RequestError:
#                     st.error("Could not request results from speech recognition service")
#                     return None
#         except Exception as e:
#             st.error(f"Error accessing microphone: {str(e)}")
#             return None

# def initialize_session_state():
#     if 'messages' not in st.session_state:
#         st.session_state.messages = []
#     if 'conversation_agent' not in st.session_state:
#         st.session_state.conversation_agent = ConversationalAgent()
#     if 'validation_agent' not in st.session_state:
#         st.session_state.validation_agent = ValidationAgent()
#     if 'script_generator' not in st.session_state:
#         st.session_state.script_generator = HypnosisScriptGenerator()
#     if 'voice_handler' not in st.session_state:
#         st.session_state.voice_handler = VoiceHandler()
#     if 'is_recording' not in st.session_state:
#         st.session_state.is_recording = False
#     if 'script_generated' not in st.session_state:
#         st.session_state.script_generated = False

# def display_chat_message(message):
#     with st.chat_message(message["role"], avatar="🧘" if message["role"] == "assistant" else "👤"):
#         st.write(message["content"])

# def handle_user_input(user_input: str):
#     # Add user message to chat
#     st.session_state.messages.append({"role": "user", "content": user_input})
    
#     # Get conversation agent's response
#     with st.spinner("Thinking..."):
#         response = st.session_state.conversation_agent.get_next_response(user_input)
#         st.session_state.messages.append({"role": "assistant", "content": response})
    
#     # Check if all questions are answered
#     if not st.session_state.script_generated:
#         conversation_history = st.session_state.conversation_agent.get_conversation_history()
#         is_complete = st.session_state.validation_agent.validate_conversation(conversation_history)
        
#         if is_complete:
#             with st.spinner("Generating your personalized hypnosis script..."):
#                 script = st.session_state.script_generator.generate_script(
#                     conversation_history=conversation_history,
#                     datetime=CURRENT_TIME
#                 )
#                 st.session_state.script_generated = True
#                 st.session_state.messages.append({
#                     "role": "assistant",
#                     "content": "Thank you for sharing all the information. Here's your personalized hypnosis script:"
#                 })
#                 st.session_state.messages.append({"role": "assistant", "content": script})

# def main():
#     st.title("AI Hypnosis Consultation")
    
#     initialize_session_state()
    
#     # Sidebar
#     with st.sidebar:
#         st.write(f"Current User: {CURRENT_USER}")
#         st.write(f"Current Time (UTC): {CURRENT_TIME}")
        
#         if st.button("Start New Chat"):
#             st.session_state.messages = []
#             st.session_state.script_generated = False
#             st.session_state.is_recording = False
#             st.session_state.conversation_agent = ConversationalAgent()
#             st.rerun()
        
#         input_method = st.radio(
#             "Choose Input Method",
#             ["Text", "Voice"],
#             key="input_method"
#         )

#     # Display chat messages
#     for message in st.session_state.messages:
#         display_chat_message(message)

#     # Initialize chat with welcome message if empty
#     if not st.session_state.messages:
#         welcome_message = {
#             "role": "assistant",
#             "content": (
               
#                 f"I'll help you create a personalized hypnosis script. Let's begin our conversation to understand your needs better."
#             )
#         }
#         st.session_state.messages.append(welcome_message)
#         initial_response = st.session_state.conversation_agent.get_next_response(
#             "Start the conversation by asking the first question."
#         )
#         st.session_state.messages.append({"role": "assistant", "content": initial_response})
#         st.rerun()

#     # Voice input handling
#     if input_method == "Voice":
#         col1, col2 = st.columns(2)
        
#         with col1:
#             if not st.session_state.is_recording:
#                 if st.button("🎤 Start Recording"):
#                     st.session_state.is_recording = True
#                     st.rerun()
        
#         with col2:
#             if st.session_state.is_recording:
#                 if st.button("⏹️ Stop Recording"):
#                     with st.spinner("Processing voice input..."):
#                         transcript = st.session_state.voice_handler.record_audio()
#                         st.session_state.is_recording = False
                        
#                         if transcript:
#                             # Display transcript
#                             st.info(f"You said: {transcript}")
#                             handle_user_input(transcript)
#                             st.rerun()
        
#         # Show recording status
#         if st.session_state.is_recording:
#             st.markdown("🔴 Recording... Speak now and click 'Stop Recording' when done.")

#     # Text input handling
#     if input_method == "Text":
#         if prompt := st.chat_input("Type your response here..."):
#             handle_user_input(prompt)
#             st.rerun()

# if __name__ == "__main__":
#     main()



# # main.py
import streamlit as st
from datetime import datetime
from agents import ConversationalAgent, ValidationAgent, HypnosisScriptGenerator
from models import ChatMessage
import speech_recognition as sr
from typing import Optional
import time
from openai import OpenAI


# Constants
CURRENT_TIME = "2025-02-03 14:56:58"
CURRENT_USER = "alokyadav2020"
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversation_agent' not in st.session_state:
        st.session_state.conversation_agent = ConversationalAgent()
    if 'validation_agent' not in st.session_state:
        st.session_state.validation_agent = ValidationAgent()
    if 'script_generator' not in st.session_state:
        st.session_state.script_generator = HypnosisScriptGenerator()
    if 'script_generated' not in st.session_state:
        st.session_state.script_generated = False
    if 'last_audio' not in st.session_state:
        st.session_state.last_audio = None

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
    
    # Check if all questions are answered
    if not st.session_state.script_generated:
        conversation_history = st.session_state.conversation_agent.get_conversation_history()
        is_complete = st.session_state.validation_agent.validate_conversation(conversation_history)
        
        if is_complete:
            with st.spinner("Generating your personalized hypnosis script..."):
                script = st.session_state.script_generator.generate_script(
                    conversation_history=conversation_history,
                    datetime=CURRENT_TIME
                )
                st.session_state.script_generated = True
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Thank you for sharing all the information. Here's your personalized hypnosis script:"
                })
                st.session_state.messages.append({"role": "assistant", "content": script})
def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript


def main():
    st.title("AI Hypnosis Consultation")
    
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.write(f"Current User: {CURRENT_USER}")
        st.write(f"Current Time (UTC): {CURRENT_TIME}")
        
        if st.button("Start New Chat"):
            st.session_state.messages = []
            st.session_state.script_generated = False
            st.session_state.conversation_agent = ConversationalAgent()
            st.session_state.last_audio = None
            st.rerun()
        
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
    if not st.session_state.messages:
        welcome_message = {
            "role": "assistant",
            "content": (
                f"I'll help you create a personalized hypnosis script. Let's begin our conversation to understand your needs better."
            )
        }
        st.session_state.messages.append(welcome_message)
        initial_response = st.session_state.conversation_agent.get_next_response(
            "Start the conversation by asking the first question."
        )
        st.session_state.messages.append({"role": "assistant", "content": initial_response})
        st.rerun()

    # Input handling
    if input_method == "Voice":
        # Using st.audio_input for voice recording
        audio_bytes = st.audio_input("Record your message")
        # audio_bytes = audio_recorder(pause_threshold=2.0, sample_rate=41_000)
        
        # Check if new audio is recorded
        if audio_bytes is not None and audio_bytes != st.session_state.last_audio:
            # st.session_state.last_audio = audio_bytes
            
            st.session_state.last_audio = st.audio(audio_bytes, format="audio/wav")
            
            with st.spinner("Processing your voice input..."):
                # Here you would typically process the audio and get the transcript
                # For now, we'll use a placeholder text
                # transcript = "Your voice message has been recorded"  # This is a placeholder
                try:
                    # transcript = sr.recognizer.recognize_google(st.session_state.last_audio)
                    transcript = speech_to_text(audio_bytes)
                    if transcript:
                        # Show transcript
                        st.info(f"You said: {transcript}")
                        # Process the input
                        handle_user_input(transcript)
                        st.rerun()
                    
                except sr.UnknownValueError:
                    st.error("Could not understand the audio. Please try again.")
                   
                except sr.RequestError:
                    st.error("Could not request results from speech recognition service")
                   
                except Exception as e:
                    st.error(f"Error accessing microphone: {str(e)}")
                
                

    else:  # Text input
        if prompt := st.chat_input("Type your response here..."):
            handle_user_input(prompt)
            st.rerun()

if __name__ == "__main__":
    main()




