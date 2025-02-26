# agents.py
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory
from src.prompts import CONVERSATION_PROMPT, VALIDATION_PROMPT, SCRIPT_GENERATION_PROMPT
from langchain_deepseek import ChatDeepSeek
import streamlit as st

class ConversationalAgent:
    def __init__(self,llm_name:str):
        if llm_name == "openai":
            self.llm = ChatOpenAI(model="gpt-4o",max_completion_tokens=500, api_key=st.secrets['OPENAI_API_KEY'],temperature=0)
        elif llm_name == "anthropic":
           self.llm = ChatAnthropic(model_name="claude-3-5-sonnet-latest",max_tokens_to_sample=500,api_key=st.secrets['ANTHROPIC_API_KEY'],temperature=0)
        elif llm_name == "deepseek":
            self.llm = ChatDeepSeek(model_name="deepseek-chat",max_tokens=500,api_key=st.secrets['DEEPSEEK_API_KEY'],temperature=0)
        self.CONVERSATION_PROMPT = CONVERSATION_PROMPT    
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.CONVERSATION_PROMPT ,
            verbose=False
        )

    def get_next_response(self, user_input: str = None) -> str:
        if user_input is None:
            print("user_input None")
            return self.conversation.predict(
                input="Start the conversation through prompt questions."
            )
        print(f"user_input : {user_input}")
        return self.conversation.predict(
            input=user_input,
            history = self.memory.chat_memory.messages
        )

    def get_conversation_history(self) -> dict:
        return {
            'memory': self.memory.chat_memory.messages,
            'user_info': self.memory.chat_memory.messages
        }

class ValidationAgent:
    def __init__(self):
        self.llm = ChatAnthropic(model_name="claude-3-5-sonnet-latest",api_key=st.secrets['ANTHROPIC_API_KEY'],temperature=0)
        self.VALIDATION_PROMPT = VALIDATION_PROMPT
        self.validation_chain = LLMChain(
            llm=self.llm,
            prompt=self.VALIDATION_PROMPT,
            verbose=False
        )

    def validate_conversation(self, conversation_history: dict) -> bool:
        result = self.validation_chain.run(conversation_history=str(conversation_history))
        return result.strip().lower() == "true"

class HypnosisScriptGenerator:
    def __init__(self,llm_name:str):
        if llm_name == "openai":
            self.llm = ChatOpenAI(model="gpt-4o",max_completion_tokens=6000, api_key=st.secrets['OPENAI_API_KEY'],temperature=0)
        elif llm_name == "anthropic":
           self.llm = ChatAnthropic(model_name="claude-3-5-sonnet-latest",max_tokens_to_sample=6000,api_key=st.secrets['ANTHROPIC_API_KEY'],temperature=0)
        elif llm_name == "deepseek":
            self.llm = ChatDeepSeek(model_name="deepseek-reasoner",max_tokens=6000,api_key=st.secrets['DEEPSEEK_API_KEY'],temperature=0)

        self.SCRIPT_GENERATION_PROMPT = SCRIPT_GENERATION_PROMPT    
            
        self.script_chain = LLMChain(
            llm=self.llm,
            prompt=self.SCRIPT_GENERATION_PROMPT
        )

    def generate_script(self, conversation_history: dict) -> str:
        return self.script_chain.run(
            conversation_history=str(conversation_history)
        )