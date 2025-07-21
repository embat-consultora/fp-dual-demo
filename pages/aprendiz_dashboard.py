from navigation import make_sidebar_aprendiz
import streamlit as st
from page_utils import apply_page_config
from streamlit_extras.stylable_container import stylable_container
from streamlit_calendar import calendar
from datetime import datetime
import pandas as pd
from sheet_connection import get_google_sheet
from data_utils import getColumns,create_events,crearAgenda
from variables import connectionGeneral
from variables import registroAprendices, recursosUtiles,formsLinks, tabPreOnboarding, tabCierre,tabOnboarding,tabSeguimiento, preOnboardingLinks, onboardingLinks,seguimientoLinks,cierreLinks, aprendiz_looker_url, presupuesto_looker_url,aprendiz_2025_looker_url,tabFeedback,tituloCalendario,tituloOrganizacion
st.session_state["current_page"] = "admin_recursos_tutor_dashboard"
apply_page_config()

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Sesion expirada. Redirigiendo a login...")
    st.session_state.logged_in = False 
    st.session_state.redirected = True 
    st.switch_page("streamlit_app.py")
else:
    if st.session_state.role == 'aprendiz':
        make_sidebar_aprendiz()
#leer el style.css 
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#get events
columns_to_extract = ['CANDIDATOS','FECHA INICIO real', 'FECHA FIN real','Envío 1er Feedback','Envío 2do Feedback','Envío 3er Feedback']
def getInfo():
    # Use the actual Google Sheets ID here
    sheet_id = registroAprendices
    df = get_google_sheet(connectionGeneral,sheet_id)
    return df

def getEvents(df):
    selected_columns_df = getColumns(df, columns_to_extract)
    selected_columns_df = selected_columns_df.drop_duplicates(subset=[columns_to_extract[0]])
    return selected_columns_df


candidatosByTutor = getInfo()
eventsCandidatos = getEvents(candidatosByTutor)
events = create_events(eventsCandidatos, columns_to_extract)

# Create the main container for the layout
container = st.container()
# Create two columns inside the container, one taking 60% width and the other 40%
st.markdown(
    """
    <style>
    .resource-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
# In the 60% container, you can place some text or content
st.subheader("Impulsa tu desarrollo con estos recursos")
# Create two side-by-side containers inside col1

# Add content to the first inner column
with stylable_container(
    key="documentation_container",
    css_styles="""
        {
            border: 1px solid rgba(49, 51, 63, 0.2);
            border-radius: 0.5rem;
            padding: calc(1em - 1px);
            background-color: white;
        }
        """,
):
    tabs = st.tabs(["Quienes somos?", "Onboarding","Links revelantes"])

# Pre-Onboarding Tab
with tabs[0]:
    st.write("Conoce la empresa")
    st.write(f"[{preOnboardingLinks[0]}]({preOnboardingLinks[1]})")
# Onboarding Tab
with tabs[1]:
    st.write("Conoce a tu tutor/a:")
    st.write("Email: maria@gmail.com")
    st.write(f"[Perfil Maria](https://drive.google.com/file/d/1YmRwMGfMzSM9LxmCRCOPFypPROg1dUi9/view?usp=sharing)")
# forms tab
with tabs[2]:
    st.write("**Aprendiz:**")
    st.write(f"[{formsLinks[0]}]({formsLinks[1]})")
    st.write(f"[{formsLinks[2]}]({formsLinks[3]})")
    st.write(f"[{formsLinks[4]}]({formsLinks[5]})")
    st.write(f"[{formsLinks[6]}]({formsLinks[7]})")
    st.write(f"[{formsLinks[8]}]({formsLinks[9]})")
    st.write(f"[{formsLinks[10]}]({formsLinks[11]})")

with st.container():
    events = events
    today = datetime.today().strftime('%Y-%m-%d')
    calendar_options = {
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridDay,dayGridWeek,dayGridMonth",
        },
        "initialDate": today,
        "initialView": "dayGridMonth",
        "locale":"ES",
        "selectable": True,
    }
    custom_css = """
        .fc-toolbar-title {
            font-size: 1.5rem;  /* Adjust the title size */
        }
        .fc {
            width: 70%;  /* Set calendar width to 70% of the container for desktop */
            margin: 0 auto;
        }
        .fc-view {
            min-height: 250px;  /* Set a minimum height */
        }
        
        /* Responsive adjustments for smaller screens */
        @media only screen and (max-width: 768px) {
            .fc {
                width: 100%;  /* Full width for mobile */
            }
            .fc-toolbar-title {
                font-size: 1.2rem;  /* Adjust the title size for mobile */
            }
        }
    """
    # Display the subheader with the current month and year
    st.subheader(tituloCalendario)
    details_placeholder = st.empty()
    # Create a dictionary to hold events by date
    # Display the calendar
    selected_date = calendar(
        events,  # Pass the event dictionary
        options=calendar_options,
        custom_css=custom_css,
        callbacks = ["eventClick"]
    )

    if selected_date:
    # Find the event details
        details_placeholder.markdown(f"**Evento:** {selected_date['eventClick']['event']['title']}\n**Dia:** {selected_date['eventClick']['event']['start']}")


