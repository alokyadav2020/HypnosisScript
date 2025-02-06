# models.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ChatMessage:
    role: str
    content: str
    timestamp: str

@dataclass
class UserInfo:
    name: str = ""
    age: str = ""