# session_manager.py
from dataclasses import dataclass
from typing import List, Dict
from models import ChatMessage
from agents import ConversationalAgent, ValidationAgent, HypnosisScriptGenerator

@dataclass
class ChatSession:
    messages: List[ChatMessage]
    conversation_agent: ConversationalAgent
    validation_agent: ValidationAgent
    script_generator: HypnosisScriptGenerator
    script_generated: bool = False

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, ChatSession] = {}
        
    def create_session(self, session_id: str) -> ChatSession:
        session = ChatSession(
            messages=[],
            conversation_agent=ConversationalAgent(),
            validation_agent=ValidationAgent(),
            script_generator=HypnosisScriptGenerator()
        )
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> ChatSession:
        return self.sessions.get(session_id)

    def delete_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]