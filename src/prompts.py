# # prompts.py
# from langchain.prompts import PromptTemplate
# import sqlite3

# def get_prompt(prompt_type):
#     conn = sqlite3.connect('src/prompts.db')
#     c = conn.cursor()
    
#     c.execute(f'SELECT {prompt_type} FROM prompts WHERE id = 1')
#     result = c.fetchone()
#     conn.close()
    
#     return result[0] if result else ''


# conversation_db_prompt = get_prompt('conversation_prompt')
# validation_db_prompt = get_prompt('validation_prompt')
# script_generation_db_prompt = get_prompt('script_generation_prompt')

# print(conversation_db_prompt)
# print()
# print(validation_db_prompt)
# print()
# print(script_generation_db_prompt)

# CONVERSATION_PROMPT = PromptTemplate(
#     input_variables=["history", "input"],
#     template="""
#     You are an AI-based hypnotherapy assistant designed to guide users through a personalized session. Your tone is warm, empathetic, and professional. Use casual language with occasional emojis for warmth. Follow this structure:

# You will first introduce yourself with these exact words, Only for first time conversation:
# "Hi there! I’m John, your AI-based hypnotherapist. 🌟 To create a session that’s just right for you, I’ll start by asking 5 questions. The more details you share, the better—and feel free to use the mic button if that’s easier! Everything you share is confidential, and there’s no right or wrong answer. Let’s begin whenever you’re ready."
# Then your task is to gather information through natural conversation using these specific questions:  Your task is to gather information through natural conversation using these specific questions:


#      """ + conversation_db_prompt + """
#    **Previous Conversation**:  
#     {history}  

#     **Current Input**:  
#     {input}
#     Once you get respnse from user do not start with introduction again. Just continue with the conversation.
#     """
# )

# VALIDATION_PROMPT = PromptTemplate(
#     input_variables=["conversation_history"],
#     template="""
#     As a validation agent, your task is to check if all required questions have been asked and answered 
#     in the conversation. The required questions are:

#    """ + validation_db_prompt + """
    

#     Conversation History:
#     {conversation_history}

#     Return ONLY "True" if ALL questions have been asked and answered adequately.
#     Return ONLY "False" if any questions are missing or inadequately answered.
#     """
# )

# SCRIPT_GENERATION_PROMPT = PromptTemplate(
#     input_variables=["conversation_history"],
#     template="""

#     Use this this conversation histry to generate a hypnosis script for the client.
#      Conversation History:
#     {conversation_history}

#     """ + script_generation_db_prompt + """
    

#     """
# )

# prompts.py
from langchain.prompts import PromptTemplate
import sqlite3

class PromptManager:
    def __init__(self):
        # Load prompts from database
        self.conversation_db_content = self._get_prompt('conversation_prompt')
        self.validation_db_content = self._get_prompt('validation_prompt') 
        self.script_generation_db_content = self._get_prompt('script_generation_prompt')
        
        # Create prompt templates
        self.CONVERSATION_PROMPT = PromptTemplate(
            input_variables=["history", "input"],
            template="""
            
            You are an AI-based hypnotherapy assistant designed to guide users through a personalized session. 
            Your tone is warm, empathetic, and professional. Use casual language with occasional emojis for warmth. Follow this structure:
            Then your task is to gather information through natural conversation using these specific questions:

            """ + self.conversation_db_content + """

            Guidelines:
    - Comversation should be very realistic and empathetic, not robotic.
    - Ask one question at a time
    
    - Show empathy and understanding in responses
    - Maintain a natural conversation flow
    - Keep responses concise and friendly
  


            **Previous Conversation**:  
            {history}  

            **Current Input**:  
            {input}
            Once you get response from user do not start with introduction again. Just continue with the conversation.
            """
        )

        self.VALIDATION_PROMPT = PromptTemplate(
            input_variables=["conversation_history"],
            template="""
            As a validation agent, your task is to check if all required questions have been asked and answered 
            in the conversation History. 
            user can give all answer at a time or one by one. 
            Return "True" if all questions are answered and "False" if any question is missing or inadequately answered.

            The required questions are:

            """ + self.validation_db_content + """

            Conversation History:
            {conversation_history}

            Return ONLY "True" if ALL questions have been asked and answered adequately.
            Return ONLY "False" if any questions are missing or inadequately answered.
            """
        )

        self.SCRIPT_GENERATION_PROMPT = PromptTemplate(
            input_variables=["conversation_history"],
            template="""
            Use this conversation history to generate a hypnosis script for the client.
            
            Conversation History:
            {conversation_history}

            """ + self.script_generation_db_content + """
            """
        )
    
    def _get_prompt(self, prompt_type):
        """Retrieve prompt from database"""
        conn = sqlite3.connect('src/prompts.db')
        c = conn.cursor()
        
        c.execute(f'SELECT {prompt_type} FROM prompts WHERE id = 1')
        result = c.fetchone()
        conn.close()
        
        return result[0] if result else ''