from navigation import make_sidebar_tutor,make_sidebar_admin
import streamlit as st
from page_utils import apply_page_config
from streamlit_carousel import carousel
st.session_state["current_page"] = "agenda_dc"
apply_page_config()

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Sesion expirada. Redirigiendo a login...")
    st.session_state.logged_in = False 
    st.session_state.redirected = True 
    st.switch_page("streamlit_app.py")
else:
    if st.session_state.role == 'tutor':
        make_sidebar_tutor()
    else:
        make_sidebar_admin()


#leer el style.css 
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.subheader("Agenda")

carousel_items = []  # Initialize as an empty list

carousel_items.append({
    "title": "",
    "text": "",
    "img": "./images/agenda_1_DC.png"
})
carousel_items.append({
    "title": "",
    "text": "",
    "img": "./images/agenda_2_DC.png"
})

# Print to ver

carousel(items=carousel_items, container_height= 1100)
