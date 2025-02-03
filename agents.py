# agents.py
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory
from prompts import CONVERSATION_PROMPT, VALIDATION_PROMPT, SCRIPT_GENERATION_PROMPT
import streamlit as st

class ConversationalAgent:
    def __init__(self):
        self.llm = ChatAnthropic(model_name="claude-3-5-sonnet-latest",max_tokens_to_sample=500,api_key=st.secrets['ANTHROPIC_API_KEY'],temperature=0.7)
        # self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=st.secrets['OPENAI_API_KEY'],temperature=0.7)
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=CONVERSATION_PROMPT,
            verbose=False
        )

    def get_next_response(self, user_input: str = None) -> str:
        if user_input is None:
            return self.conversation.predict(
                input="Start the conversation by introducing yourself and asking for the user's name."
            )
        return self.conversation.predict(input=user_input)

    def get_conversation_history(self) -> dict:
        return {
            'memory': self.memory.chat_memory.messages,
            'user_info': self.memory.chat_memory.messages
        }

class ValidationAgent:
    def __init__(self):
        self.llm = ChatAnthropic(model_name="claude-3-5-sonnet-latest",api_key=st.secrets['ANTHROPIC_API_KEY'],temperature=0)
        self.validation_chain = LLMChain(
            llm=self.llm,
            prompt=VALIDATION_PROMPT,
            verbose=False
        )

    def validate_conversation(self, conversation_history: dict) -> bool:
        result = self.validation_chain.run(conversation_history=str(conversation_history))
        return result.strip().lower() == "true"

class HypnosisScriptGenerator:
    def __init__(self):
        self.llm = ChatAnthropic(model_name="claude-3-5-sonnet-latest",api_key=st.secrets['ANTHROPIC_API_KEY'],temperature=0.7)
        self.script_chain = LLMChain(
            llm=self.llm,
            prompt=SCRIPT_GENERATION_PROMPT
        )

    def generate_script(self, conversation_history: dict, datetime: str) -> str:
        return self.script_chain.run(
            conversation_history=str(conversation_history),
            datetime=datetime
        )