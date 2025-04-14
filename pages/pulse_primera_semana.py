import streamlit as st
import json
from streamlit_gsheets import GSheetsConnection
from sheet_connection import get_all_worksheets
from variables import connectionFeedbacks, worksheetPulse1Semana,autocompletarTutor,autocompletarNombre,page_icon
from data_utils import is_valid_email
import pandas as pd
import logging

def run():
    st.set_page_config(
        page_title="Formulario 1º Semana",
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
    'form_completed': False,
}
for key, value in default_values.items():
    st.session_state.setdefault(key, value)

# Load quiz data
with open('content/formularioPulse1Semana.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

# Define pages and their questions
pageOneQuestions = range(0, 3)  # Questions for page 1
pageTwoQuestions = range(3, 6)  # Questions for page 2
pages = [pageOneQuestions, pageTwoQuestions]

# Total number of questions
total_questions = len(quiz_data["text_form"]["questions"])

def submit_answer(question_index, response):
    st.session_state.responses[question_index] = response  # Use the index to maintain order

def next_question():
    st.session_state.current_page += 1
    print('next pregunta')

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
    # Collect responses in order
    responses_only = [
        data.get(idx, "")  # Fetch responses by index to maintain the order
        for idx in range(total_questions)
    ]
    responses_only.append(autocompletarTutor)
    responses_only.append(autocompletarNombre)
    conn = create_gsheets_connection()
    existing_data = conn.read(worksheet=worksheetPulse1Semana)
    new_row = pd.DataFrame([responses_only], columns=existing_data.columns)  # Ensure column names match
    # Concatenate the new row with existing data
    updated_data = pd.concat([existing_data, new_row], ignore_index=True)
    conn.update(worksheet=worksheetPulse1Semana, data=updated_data)
    logging.info("Submitting successfully")

def all_questions_answered():
    current_page_questions = pages[st.session_state.current_page]
    for idx in current_page_questions:
        if idx not in st.session_state.responses or not st.session_state.responses[idx]:
            return False
    return True

# Check if the form is completed
if st.session_state.form_completed:
    st.title("¡Formulario Completado!")
    st.success("Las respuestas se guardaron exitosamente!")
    st.write(quiz_data["text_form"]["cierre"])
else:
    st.title(quiz_data["text_form"]["title"])
    st.write(quiz_data["text_form"]["description"])

    current_question_index = sum(len(pages[i]) for i in range(st.session_state.current_page))
    progress_bar_value = current_question_index / total_questions
    st.progress(progress_bar_value)

    current_page_questions = pages[st.session_state.current_page]
    for idx in current_page_questions:
        previous_response = st.session_state.responses.get(idx, None)
        question_item = quiz_data["text_form"]["questions"][idx]
        st.subheader(question_item['question'])
        
        if "options" in question_item and question_item["options"]:
            response = st.selectbox(
            "Seleccione una opción:",
            question_item["options"],
            key=f"response_{idx}",
            index=question_item["options"].index(previous_response) if previous_response in question_item["options"] else 0,
        )
        else:
            response = st.text_input(
            "Respuesta",
            key=f"response_{idx}",
            value=previous_response if previous_response is not None else "",
        )
        
        if question_item['id'] == 'q1':
            if response and not is_valid_email(response):
                st.error("Por favor, ingresa un correo electrónico válido.")
                email_valid = False
            else:
                email_valid = True
        if response:
            submit_answer(idx, response)  # Use index for consistent ordering

    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.current_page > 0:
            st.button("Anterior", on_click=lambda: setattr(st.session_state, 'current_page', st.session_state.current_page - 1))

    with col2:
        if st.session_state.current_page < len(pages) - 1:
            if st.button("Continuar", on_click=next_question, disabled=not (email_valid and all_questions_answered())):
                if all_questions_answered():
                    st.session_state.current_page += 1
                else:
                    st.warning("Por favor responde todas las preguntas en esta página antes de continuar.")
        else:
            if st.button("Completar", disabled=not (all_questions_answered())):
                if all_questions_answered():
                    with st.spinner("Guardando las respuestas, por favor espera..."):
                        save_to_google_sheet(st.session_state.responses)
                        st.success("Las respuestas se guardaron exitosamente!")
                        st.session_state.form_completed = True
                        st.rerun()
                else:
                    st.warning("Por favor responde todas las preguntas antes de completar.")
