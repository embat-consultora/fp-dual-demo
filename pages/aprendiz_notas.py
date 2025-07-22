from navigation import make_sidebar_aprendiz
import streamlit as st
from page_utils import apply_page_config
from sheet_connection import get_google_sheet
from variables import connectionGeneral
from variables import registroAprendices
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

candidatosByTutor = getInfo()

df_filtrado = candidatosByTutor[candidatosByTutor["CORREO DE CONTACTO"] == "usuario2@email.com"]
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
st.subheader("Te escuchamos")
# Create two side-by-side containers inside col1
st.write("Dejale un comentario a tu tutor")
# Lista de departamentos
departamentos = [
    "Cocina", "Economato", "Administracion", 
    "Recepción", "Pisos", "SSTT", "Guest Service"
]

# Estado inicial para guardar notas por departamento
if "notas_por_depto" not in st.session_state:
    st.session_state.notas_por_depto = {d: "" for d in departamentos}

# Dropdown para seleccionar departamento
departamento_seleccionado = st.selectbox("Seleccioná un departamento:", departamentos)

nota_actual = st.session_state.notas_por_depto.get(departamento_seleccionado, "")

# Si el campo está vacío y el departamento es SSTT, asignar nota por defecto
if nota_actual.strip() == "" and departamento_seleccionado == "SSTT":
    nota_actual = "No tengo la documentacion necesaria. \n Tutor: Te enviaremos todo a tu email"

# Mostrar área de texto con ese valor
nota = st.text_area(
    f"Notas para {departamento_seleccionado}:",
    value=nota_actual,
    key=departamento_seleccionado
)
# Guardar la nota en la sesión al hacer clic
if st.button("Guardar nota"):
    st.session_state.notas_por_depto[departamento_seleccionado] = nota
    st.success(f"Nota guardada para {departamento_seleccionado} ✅")
