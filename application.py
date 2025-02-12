import streamlit as st
import os
from pathlib import Path


if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None,"Admin"]


def login():

    # st.header("Log in")
    # role = st.selectbox("Choose your role", ROLES)
    with st.form("Login Form", clear_on_submit=True):
        st.write("Login Form")
        
        # Username and password inputs
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        # Submit button
        submit_button = st.form_submit_button("Login",use_container_width=True)
        
        # Check if the form was submitted
        if submit_button:

            if st.secrets['USER'] == username and st.secrets['PASSWORD'] == password:
                st.session_state.role = "Admin"
                st.success("Login successful!")
                st.session_state["logged_in"] = True
                st.rerun()
            # Check if username and password are correct
            # result = userloging(username.strip(),password.strip())

            
            # print(result)
            # if result is not None:
            #     st.success("Login successful!")
            #     st.session_state["logged_in"] = True  # Track login status with session state
            #     st.session_state["user_id"] = result[0]
            #     st.session_state['permission'] = result[1]
            #     st.session_state['Isactive'] = result[2]
            #     st.session_state["user_email"] = result[3]
            #     st.session_state.role = result[4]
            #     st.rerun()
                

    # if st.button("Log in"):
    #     st.session_state.role = role
    #     st.rerun()


def logout():
    st.session_state.role = None
    st.rerun()


role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
# settings = st.Page(os.path.join("streamlit","setting.py"), title="Settings", icon=":material/settings:")
# file_managemet = st.Page(
#     Path("streamlit/User/ProcessPDF.py"),
#     title="File management",
#     icon=":material/help:",
#     default=(role == "User"),
# )
# Project = st.Page(os.path.join("streamlit/User","Project.py"), title="Project", icon=":material/handyman:"
# )

# File_processing = st.Page(os.path.join("streamlit/User","FileProcessiong.py"),title="File Processing", icon=":material/handyman:")
# upload_pdf_files = st.Page(os.path.join("streamlit/User","uploadPdfFile.py"),title="Upload files", icon=":material/handyman:")
# runsheet_file = st.Page(os.path.join("streamlit/User","runsheet_test.py"),title="Runsheet", icon=":material/handyman:")
# Display_Project = st.Page(os.path.join("streamlit/User","OCR_PDF_FILE_DETAILS.py"),title="OCR Details", icon=":material/handyman:")
# Chain_Of_Title = st.Page(os.path.join("streamlit/User","Chain_Of_Title.py"),title="Chain Of Title", icon=":material/handyman:")

admin_1 = st.Page(os.path.join("streamlit","app.py"),title="Hypnosis",icon=":material/security:",default=(role == "Admin"),)
admin_2 = st.Page(os.path.join("streamlit","setting.py"), title="Prompt",icon=":material/person_add:" )


account_pages = [logout_page]
# user_page = [Project,runsheet_file,Display_Project,Chain_Of_Title]

admin_pages = [admin_1, admin_2]

# st.title("Request man")
# st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

page_dict = {}

if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()