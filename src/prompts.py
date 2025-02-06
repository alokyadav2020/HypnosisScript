# prompts.py
from langchain.prompts import PromptTemplate
import sqlite3

def get_prompt(prompt_type):
    conn = sqlite3.connect('src/prompts.db')
    c = conn.cursor()
    
    c.execute(f'SELECT {prompt_type} FROM prompts WHERE id = 1')
    result = c.fetchone()
    conn.close()
    
    return result[0] if result else ''



CONVERSATION_PROMPT = PromptTemplate(
    input_variables=["history", "input"],
    template=f"""
    you are AI-assisted hypnotherapy companion, an empathetic and professional hypnotherapy consultation assistant.
    Your task is to gather information through natural conversation using these specific questions:
    

    {get_prompt('conversation_prompt')}

    **Previous Conversation**:  
    {{history}}  

    **Current Input**:  
    {{input}}
    """
)

VALIDATION_PROMPT = PromptTemplate(
    input_variables=["conversation_history"],
    template=f"""
    As a validation agent, your task is to check if all required questions have been asked and answered 
    in the conversation. The required questions are:

   {get_prompt('validation_prompt')}
    

    Conversation History:
    {{conversation_history}}

    Return ONLY "True" if ALL questions have been asked and answered adequately.
    Return ONLY "False" if any questions are missing or inadequately answered.
    """
)

SCRIPT_GENERATION_PROMPT = PromptTemplate(
    input_variables=["conversation_history"],
    template=f"""

    Use this this conversation histry to generate a hypnosis script for the client.
     Conversation History:
    {{conversation_history}}

      {get_prompt('script_generation_prompt')}

    """
)