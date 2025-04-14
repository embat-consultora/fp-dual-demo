import streamlit as st
import json
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from variables import folderIdTutor,worksheetPerfilTutor, smileFacePath, rocketPath, camaraPath,connectionFeedbacks,page_icon
from data_utils import is_valid_email
import logging
from sheet_connection import upload_to_drive,get_all_worksheets
def run():
    st.set_page_config(
        page_title="Formulario FP Dual",
        page_icon=page_icon,
        layout="centered",
    )

    st.image("./images/logoCreciendoJuntos.png", width=250)

if __name__ == "__main__":
    run()

# Custom CSS for the buttons
st.markdown("""
<style>
div.stButton > button:first-child {
    display: block;
    margin: 0 auto;
</style>
""", unsafe_allow_html=True)

default_values = {
    'current_page': 0,
    'responses': {},
    'form_completed': False,  # Flag to track if the form is completed
    'photo_uploaded': False 
}
for key, value in default_values.items():
    st.session_state.setdefault(key, value)

# Load quiz data
with open('content/formulario_perfil_tutor.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

# Define pages and their questions
pageOneQuestions = range(0, 5)  # Questions for page 1
pageTwoQuestions = range(5, 9)  # Questions for page 2
pages = [pageOneQuestions, pageTwoQuestions]

# Total number of questions
total_questions = len(quiz_data["text_form"]["questions"])

def submit_answer(question_id, response):
    st.session_state.responses[question_id] = response

def next_question():
    st.session_state.current_page += 1

def create_gsheets_connection():
    try:
        connFeedback = get_all_worksheets(connectionFeedbacks)
        return connFeedback
    except Exception as e:
        st.error(f"Unable to connect to storage: {e}")
        logging.error(e, stack_info=True, exc_info=True)
        return None

def save_to_google_sheet(data):
    logging.info("Submitting records")
    responses_only = list(data.values())
    conn = create_gsheets_connection()
    existing_data = conn.read(worksheet=worksheetPerfilTutor)
    new_row = pd.DataFrame([responses_only], columns=existing_data.columns)  # Ensure column names match
    
    # Concatenate the new row with existing data
    updated_data = pd.concat([existing_data, new_row], ignore_index=True)


    conn.update(worksheet=worksheetPerfilTutor, data=updated_data)
    logging.info("Submitting successfully")
    folder_id = folderIdTutor
    file_id = upload_to_drive(uploaded_photo.name, folder_id, st.session_state.responses.get('q2', ''))
    st.success(f"Archivo subido exitosamente: {file_id}")
    st.session_state.photo_uploaded = True
def all_questions_answered():
    current_page_questions = pages[st.session_state.current_page]
    for idx in current_page_questions:
        question_id = quiz_data["text_form"]["questions"][idx]["id"]
        if question_id not in st.session_state.responses or not st.session_state.responses[question_id]:
            return False
    return True

# Check if the form is completed
if st.session_state.form_completed:
    # Show the new page with success or warning message
    st.title("¡Formulario Completado!")
    st.success("Las respuestas se guardaron exitosamente!")
    st.write(quiz_data["text_form"]["cierre"])
else:
    # Title and description
    st.title(quiz_data["text_form"]["title"])
    st.write(quiz_data["text_form"]["description"])

    # Progress calculation
    current_question_index = sum(len(pages[i]) for i in range(st.session_state.current_page))
    progress_bar_value = current_question_index / total_questions
    st.progress(progress_bar_value)

    # Display questions for the current page
    current_page_questions = pages[st.session_state.current_page]
    email_valid = True
    photo_uploaded = False
    if st.session_state.current_page == 0:
        st.markdown(f"""
        <div style="display: flex; align-items: center;padding-bottom:10px">
            <img src="{smileFacePath}" style="width:60px; ">
            <h4>Algunas cosas sobre ti</h4>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.current_page == 1:
        st.markdown(f"""
        <div style="display: flex; align-items: center;padding-bottom:10px">
            <img src="{rocketPath}" style="width:60px;">
            <h4>Algunas cosas sobre el programa e Iberostar</h4>
        </div>
        """, unsafe_allow_html=True)
    for idx in current_page_questions:
        previous_response = st.session_state.responses.get(idx, None)
        question_item = quiz_data["text_form"]["questions"][idx]
        st.markdown(f"""
        <div style="display: flex; align-items: center;">
            <h6 style="margin: 0;">{question_item['question']}</h4>
        </div>
        """, unsafe_allow_html=True)

        response = st.text_input(
            "Respuesta",
            key=f"response_{idx}",
            value=previous_response if previous_response is not None else "",
        )
        
        if question_item['id'] == 'q2':
            if response:
                    response = response.upper()  # Convert the user's input to uppercase
                    if not is_valid_email(response):
                        st.error("Por favor, ingresa un correo electrónico válido.")
                        email_valid = False
                    else:
                        email_valid = True
        
        if response:
            submit_answer(question_item["id"], response)

    if st.session_state.current_page == 1:
        st.markdown(f"""
        <div style="display: flex; align-items: center;">
            <img src="{camaraPath}" style="width:60px;">
            <h4>Una Foto Tuya</h4>
        </div>
        """, unsafe_allow_html=True)
        MAX_FILE_SIZE = 10 * 1024 * 1024
        uploaded_photo = st.file_uploader("Sube una foto para tu perfil! (JPG or PNG)", type=["jpg", "png"], accept_multiple_files=False)
        if uploaded_photo is not None and not st.session_state.photo_uploaded:
            if uploaded_photo.size > MAX_FILE_SIZE:
                st.warning("El archivo es demasiado grande. El tamaño máximo permitido es de 10MB.")
            else:
                with open(uploaded_photo.name, "wb") as f:
                    f.write(uploaded_photo.read())
                photo_uploaded = True
               

    # Column layout for navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.current_page > 0:
            st.button("Anterior", on_click=lambda: setattr(st.session_state, 'current_page', st.session_state.current_page - 1))

    with col2:
        # Disable the "Completar" button if conditions are not met
        if st.session_state.current_page < len(pages) - 1:
            if st.button("Continuar", on_click=next_question, disabled=not (email_valid and all_questions_answered())):
                if all_questions_answered():
                    st.session_state.current_page += 1
                else:
                    st.warning("Por favor responde todas las preguntas en esta página antes de continuar.")
        else:
            if st.button("Completar", disabled=not (all_questions_answered() and photo_uploaded)):
                if all_questions_answered() and photo_uploaded:
                    with st.spinner("Guardando las respuestas, por favor espera..."):
                        save_to_google_sheet(st.session_state.responses)
                        st.session_state.form_completed = True  # Set the form as completed
                        st.rerun()  # Rerun the app to show the new page
                else:
                    st.warning("Por favor responde todas las preguntas y asegúrate de subir una foto antes de completar.")
