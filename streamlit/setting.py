# import streamlit as st
# import sqlite3

# # Initialize database and tables
# def init_db():
#     conn = sqlite3.connect('src/prompts.db')
#     c = conn.cursor()
    
#     # Create tables if they don't exist
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS prompt1 (
#             id INTEGER PRIMARY KEY,
#             content TEXT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#         )
#     ''')
    
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS prompt2 (
#             id INTEGER PRIMARY KEY,
#             content TEXT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#         )
#     ''')
    
#     conn.commit()
#     conn.close()

# # Save prompt to database
# def save_prompt(table_name, content):
#     conn = sqlite3.connect('src/prompts.db')
#     c = conn.cursor()
    
#     # Check if existing entry exists
#     c.execute(f'SELECT * FROM {table_name}')
#     exists = c.fetchone()
    
#     if exists:
#         # Update existing entry
#         c.execute(f'''
#             UPDATE {table_name}
#             SET content = ?, timestamp = CURRENT_TIMESTAMP
#             WHERE id = 1
#         ''', (content,))
#     else:
#         # Insert new entry
#         c.execute(f'''
#             INSERT INTO {table_name} (id, content)
#             VALUES (1, ?)
#         ''', (content,))
    
#     conn.commit()
#     conn.close()

# # Get saved prompt from database
# def get_prompt(table_name):
#     conn = sqlite3.connect('src/prompts.db')
#     c = conn.cursor()
    
#     c.execute(f'SELECT content FROM {table_name} WHERE id = 1')
#     result = c.fetchone()
#     conn.close()
    
#     return result[0] if result else ''

# # Initialize database
# init_db()

# # Streamlit UI
# st.title('Prompt Manager')

# # Prompt 1 Section
# st.subheader("Prompt 1")
# prompt1 = st.text_area("Enter Prompt 1:", value=get_prompt('prompt1'), key='prompt1')
# if st.button("Save Prompt 1"):
#     save_prompt('prompt1', prompt1)
#     st.success("Prompt 1 saved successfully!")

# # Prompt 2 Section
# st.subheader("Prompt 2")
# prompt2 = st.text_area("Enter Prompt 2:", value=get_prompt('prompt2'), key='prompt2')
# if st.button("Save Prompt 2"):
#     save_prompt('prompt2', prompt2)
#     st.success("Prompt 2 saved successfully!")

# # Display saved prompts
# st.header("Saved Prompts")

# col1, col2 = st.columns(2)
# with col1:
#     st.subheader("CONVERSATION PROMPT")
#     st.write(get_prompt('prompt1'))

# with col2:
#     st.subheader("Prompt 2")
#     st.write(get_prompt('prompt2'))

import streamlit as st
import sqlite3
st.set_page_config(
    page_title="Prompt Management System",
    layout="wide",
)

# Initialize database and table
def init_db():
    conn = sqlite3.connect('src/prompts.db')
    c = conn.cursor()
    
    # Create single table with three columns
    c.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY,
            conversation_prompt TEXT,
            validation_prompt TEXT,
            script_generation_prompt TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Save prompt to database
def save_prompt(prompt_type, content):
    conn = sqlite3.connect('src/prompts.db')
    c = conn.cursor()
    
    # Check if existing entry exists
    c.execute('SELECT * FROM prompts WHERE id = 1')
    exists = c.fetchone()
    
    if exists:
        # Update existing entry
        c.execute(f'''
            UPDATE prompts
            SET {prompt_type} = ?, timestamp = CURRENT_TIMESTAMP
            WHERE id = 1
        ''', (content,))
    else:
        # Insert new entry with empty values for other prompts
        c.execute(f'''
            INSERT INTO prompts (id, {prompt_type})
            VALUES (1, ?)
        ''', (content,))
    
    conn.commit()
    conn.close()

# Get saved prompt from database
def get_prompt(prompt_type):
    conn = sqlite3.connect('src/prompts.db')
    c = conn.cursor()
    
    c.execute(f'SELECT {prompt_type} FROM prompts WHERE id = 1')
    result = c.fetchone()
    conn.close()
    
    return result[0] if result else ''

# Initialize database
init_db()

# Streamlit UI
st.title('Prompt Management System')

# Input Section
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Conversation Prompt")
    conv_prompt = st.text_area(
        "Enter conversation prompt:",
        value=get_prompt('conversation_prompt'),
        key='conv'
    )
    if st.button("Save Conversation Prompt"):
        save_prompt('conversation_prompt', conv_prompt)
        st.success("Conversation prompt saved!")

with col2:
    st.subheader("Validation Prompt")
    valid_prompt = st.text_area(
        "Enter validation prompt:",
        value=get_prompt('validation_prompt'),
        key='valid'
    )
    if st.button("Save Validation Prompt"):
        save_prompt('validation_prompt', valid_prompt)
        st.success("Validation prompt saved!")

with col3:
    st.subheader("Script Generation Prompt")
    script_prompt = st.text_area(
        "Enter script generation prompt:",
        value=get_prompt('script_generation_prompt'),
        key='script'
    )
    if st.button("Save Script Prompt"):
        save_prompt('script_generation_prompt', script_prompt)
        st.success("Script prompt saved!")

# Display Section
st.header("Current Saved Prompts")
st.subheader("Conversation Prompt")
st.code(get_prompt('conversation_prompt'), language='text')

st.subheader("Validation Prompt")
st.code(get_prompt('validation_prompt'), language='text')

st.subheader("Script Generation Prompt")
st.code(get_prompt('script_generation_prompt'), language='text')