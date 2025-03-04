
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory,ConversationBufferWindowMemory
from src.prompts import PromptManager
from langchain_deepseek import ChatDeepSeek
import streamlit as st

class ConversationalAgent:
    def __init__(self,llm_name:str="anthropic"):
        if llm_name == "openai":
            self.llm = ChatOpenAI(model="gpt-4o",max_completion_tokens=500, api_key=st.secrets['OPENAI_API_KEY'],temperature=0.1)
        elif llm_name == "anthropic":
           self.llm = ChatAnthropic(model_name="claude-3-7-sonnet-latest",max_tokens_to_sample=500,api_key=st.secrets['ANTHROPIC_API_KEY'],temperature=0.1)
        elif llm_name == "deepseek":
            self.llm = ChatDeepSeek(model_name="deepseek-chat",max_tokens=500,api_key=st.secrets['DEEPSEEK_API_KEY'],temperature=0.1)
        self.CONVERSATION_PROMPT = PromptManager()    
        self.memory = ConversationBufferMemory(memory_key="history")
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.CONVERSATION_PROMPT.CONVERSATION_PROMPT,
            verbose=False
        )

        print("##################################################")
        print()

        print(f"conversational prompt *******PROMPT***********: {self.CONVERSATION_PROMPT.CONVERSATION_PROMPT}")
        print()
        print("##################################################")
        

    def get_next_response(self, user_input: str = None) -> str:
        if user_input is None:
            return self.conversation.predict(
                input="Follow prompt to star conversation"
            )
        return self.conversation.predict(
            input=user_input
        )
    
    def get_conversation_history(self) -> dict:
        return {
            'memory': self.memory.chat_memory.messages
        }

    

class ValidationAgent:
    def __init__(self):
        self.llm = ChatAnthropic(model_name="claude-3-7-sonnet-latest",api_key=st.secrets['ANTHROPIC_API_KEY'],temperature=0)
        self.VALIDATION_PROMPT = PromptManager()
        self.validation_chain = LLMChain(
            llm=self.llm,
            prompt=self.VALIDATION_PROMPT.VALIDATION_PROMPT,
            verbose=False
        )

    def validate_conversation(self, conversation_history: dict) -> bool:
        """Check if we have enough information to generate a hypnosis script."""
        
        print("##################################################")
        print()
        print(f"Conversation history: {conversation_history}")
        result = self.validation_chain.run(conversation_history=str(conversation_history))
        print()
        print("##################################################")
        print()
        print(f"Validation result: {result}")
        
        # More flexible check - look for any positive indicators
        result_lower = result.strip().lower()
        is_valid = (
            "true" in result_lower or 
            "yes" in result_lower or
            "complete" in result_lower or 
            "sufficient" in result_lower or
            "enough information" in result_lower
        )
        
        print(f"Is conversation valid: {is_valid}")
        return is_valid

class HypnosisScriptGenerator:
    def __init__(self,llm_name:str = "anthropic"):
        if llm_name == "openai":
            self.llm = ChatOpenAI(model="gpt-4o",max_completion_tokens=6000, api_key=st.secrets['OPENAI_API_KEY'],temperature=0)
        elif llm_name == "anthropic":
           self.llm = ChatAnthropic(model_name="claude-3-7-sonnet-latest",max_tokens_to_sample=6000,api_key=st.secrets['ANTHROPIC_API_KEY'],temperature=0)
        elif llm_name == "deepseek":
            self.llm = ChatDeepSeek(model_name="deepseek-reasoner",max_tokens=6000,api_key=st.secrets['DEEPSEEK_API_KEY'],temperature=0)

        self.SCRIPT_GENERATION_PROMPT = PromptManager()    
            
        self.script_chain = LLMChain(
            llm=self.llm,
            prompt=self.SCRIPT_GENERATION_PROMPT.SCRIPT_GENERATION_PROMPT
        )

    def generate_script(self, conversation_history: dict) -> str:
        return self.script_chain.run(
            conversation_history=str(conversation_history)
        )