from navigation import make_sidebar_tutor
import streamlit as st
import plotly.express as px
from page_utils import apply_page_config
from data_utils import filter_dataframe,filter_dataframeToUpper, create_donut_chart,generate_color_map,calcularPorcentajesStatus,feedbackColor,getColumns
from sheet_connection import get_google_sheet, get_sheets
from feedback_utils import calcularEstadoRespuestaCambioArea,getFeedbackPulse1Semana,getFeedbackPromedioCambioArea,getFeedbackPromedioPrimerMes,getFeedbackPromedioCuartoMes,getFeedbackPromedioAprendizCierrePrimerCiclo,getFeedbackPromedioAprendizCierreSegundoCiclo,calcularEstadoRespuestas
import pandas as pd
import matplotlib.pyplot as plt
from variables import cambioArea_types, anioActual,cambioAreaSheet, registroAprendices,resultadoVerde, semaforoFeedback, resultadosFeedback, resultadoAmarillo,resultadoAzul,resultadoAmarilloDetalle,resultadoAzulDetalle,resultadoVerdeDetalle, azul,feedbackTitle,detalleFeedbackTitle,feedbackSubtitle, amarillo, aquamarine,worksheetPulse1Semana, connectionGeneral, connectionFeedbacks,connectionUsuarios, rotationSheet,orange, errorRedirection, worksheetCambioArea,noDatosDisponibles, worksheetFormulario1Mes, worksheetFormulario4Mes, worksheetFormularioAprendizCierre1Ciclo, worksheetFormularioAprendizCierre2Ciclo,feedback_types,colorPulse, colorCambioArea, colorPrimerMes, colorAprendizCierrePrimerCiclo,colorAprendizCierreSegundoCiclo,colorCuartoMes,pulse1SemanaPromedio, primerMesPromedio, cuartoMesPromedio, cambioAreaPromedio, aprendizCierrePrimerCicloPromedio, aprendizCierreSegundoCicloPromedio,primerSemana, primerMes, cuartoMes,primerCierre,segundoCierre,cambioArea,dondeEstanMisAprendices
from datetime import datetime, timedelta
from streamlit_carousel import carousel
st.session_state["current_page"] = "tutor_aprendiz_dashboard"
#tab icono y titulo
apply_page_config()
#verificar si el usuario esta logueado sino redigirlo a la login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning(errorRedirection)
    st.session_state.logged_in = False 
    st.session_state.redirected = True 
    st.switch_page("streamlit_app.py")
else:
    if st.session_state.role == 'tutor':
        make_sidebar_tutor()

#leer el style.css 
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
hoy = datetime.today()
#filtros de arriba
columnaCandidatos='CANDIDATOS'
columnaFechaInicio='FECHA INICIO real'
columnaFechaFin='FECHA FIN real'
columnaHotel='HOTEL'
columnaFPDualFCT='FPDUAL / FCT'
columnaPosicion='POSICIÓN/DPT'
columnaEstudios='ESTUDIOS'
filtrosTutor = ["CORREO TUTOR", "MAIL TUTOR"]
columnaEnvio1Semana='Envío 1er Feedback'
columnaEnvio1Mes='Envío 2do Feedback'
columnaEnvio4Mes='Envío 3er Feedback'
columnaEnvioCambioArea='Form cambio de área'
columnaEnvio1Cierre='Fecha Cierre 1 er Ciclo'
columnaEnvio2Cierre='Fecha Inicio 2do ciclo'
valorFPDUALINT = "FP DUAL INT"
colorLetraPrimerSemana='black'
colorLetraCambioArea='black'
colorLetraPrimerMes='black'
colorLetraCuartoMes='black'
colorLetraPrimerCierre='black'
colorLetraSegundoCierre='blacks'
#feedback
columnaEmail='Email'
columnaCorreoCandidato='CORREO DE CONTACTO'
topFilters = [columnaFechaInicio,columnaCandidatos,columnaHotel,columnaFPDualFCT, columnaFechaFin]
columnStatus = 'STATUS'
#trae todos los datos filtrados por Tutor 
def getInfo():
    sheet_id = registroAprendices
    filters = {filtrosTutor[0]: [st.session_state.username]}
    df = get_google_sheet(connectionGeneral,sheet_id)
    dfiltered = filter_dataframe(df, filters)
    dfiltered =dfiltered.drop_duplicates(subset=[columnaCandidatos])
    return dfiltered

df = getInfo()
#parseando las fechas
df[topFilters[0]] = pd.to_datetime(df[topFilters[0]], format='%d/%m/%Y')
df[topFilters[4]] = pd.to_datetime(df[topFilters[4]], format='%d/%m/%Y')
active_candidates = df[df[columnStatus].str.upper() == 'ACTIVO']
#Container Feedback
def getFeebackDetails():
    feedbacks = get_sheets(connectionFeedbacks, [worksheetPulse1Semana,worksheetCambioArea,worksheetFormulario1Mes,worksheetFormulario4Mes, worksheetFormularioAprendizCierre1Ciclo, worksheetFormularioAprendizCierre2Ciclo])
    return feedbacks

feedbacks= getFeebackDetails()
feedbackPulseDf = None
feedbackCambioAreaDf = None
feedback1MesDf = None
feedback4MesDf = None
feedbackAprendizPrimerCierreDf = None
feedbackAprendizSegundoCierreDf = None
if feedbacks and isinstance(feedbacks, list):
        for i, feedback in enumerate(feedbacks):
            # Ensure feedback is a valid DataFrame
            if feedback is not None and isinstance(feedback, pd.DataFrame) and not feedback.empty:
                # Apply filters for each feedback category based on index
                filtered_feedback = feedback[feedback[columnaEmail].apply(
                    lambda x: x.lower() if isinstance(x, str) else None
                ).isin(
                    df[columnaCorreoCandidato].apply(lambda x: x.lower() if isinstance(x, str) else None)
                )]

                # Drop duplicates if filtered_feedback is valid
                if filtered_feedback is not None and not filtered_feedback.empty:
                    filtered_feedback = filtered_feedback.drop_duplicates(subset=[columnaEmail])
                
                # Handle feedback categories based on index
                if i == 0:
                    feedbackPulseDf = filtered_feedback
                    if feedbackPulseDf is not None and not feedbackPulseDf.empty:
                        pulse1SemanaPromedio = getFeedbackPulse1Semana(feedbackPulseDf)
                        colorPulse, colorLetraPrimerSemana = feedbackColor(pulse1SemanaPromedio)
                elif i == 1:
                    feedbackCambioAreaDf = filtered_feedback
                    if feedbackCambioAreaDf is not None and not feedbackCambioAreaDf.empty:
                        cambioAreaPromedio = getFeedbackPromedioCambioArea(feedbackCambioAreaDf)
                        colorCambioArea, colorLetraCambioArea = feedbackColor(cambioAreaPromedio)
                elif i == 2:
                    feedback1MesDf = filtered_feedback
                    if feedback1MesDf is not None and not feedback1MesDf.empty:
                        primerMesPromedio = getFeedbackPromedioPrimerMes(feedback1MesDf)
                        colorPrimerMes, colorLetraPrimerMes = feedbackColor(primerMesPromedio)
                elif i == 3:
                    feedback4MesDf = filtered_feedback
                    if feedback4MesDf is not None and not feedback4MesDf.empty:
                        cuartoMesPromedio = getFeedbackPromedioCuartoMes(feedback4MesDf)
                        colorCuartoMes, colorLetraCuartoMes = feedbackColor(cuartoMesPromedio)
                elif i == 4:
                    feedbackAprendizPrimerCierreDf = filtered_feedback
                    if feedbackAprendizPrimerCierreDf is not None and not feedbackAprendizPrimerCierreDf.empty:
                        aprendizCierrePrimerCicloPromedio = getFeedbackPromedioAprendizCierrePrimerCiclo(feedbackAprendizPrimerCierreDf)
                        colorAprendizCierrePrimerCiclo, colorLetraPrimerCierre = feedbackColor(aprendizCierrePrimerCicloPromedio)
                elif i == 5:
                    feedbackAprendizSegundoCierreDf = filtered_feedback
                    if feedbackAprendizSegundoCierreDf is not None and not feedbackAprendizSegundoCierreDf.empty:
                        aprendizCierreSegundoCicloPromedio = getFeedbackPromedioAprendizCierreSegundoCiclo(feedbackAprendizSegundoCierreDf)
                        colorAprendizCierreSegundoCiclo, colorLetraSegundoCierre = feedbackColor(aprendizCierreSegundoCicloPromedio)
else:
    st.write("No valid feedback data available for processing.")


#feedback details 

with st.container():
    st.markdown(
    f"""
    <h3 style="text-align: center; color: {azul};">
        {feedbackTitle}
    </h3>
    <p style="text-align: center; color: {azul};">{feedbackSubtitle}</p>
    """,
    unsafe_allow_html=True,
)
referencia, spacer, metricas, spacer2= st.columns([1,0.5,1,0.5])
with metricas:
        st.subheader(resultadosFeedback)
        col1,col2 = st.columns(2)
        with col1:
            with st.container():
                    st.markdown(
                        f"""
                            <div style="padding-block: 10px; border-radius: 10px; text-align: center; margin-bottom: 10px; background-color: {colorPulse};">
                                <span style="color:{colorLetraPrimerSemana}; font-size: 16px;font-weight: bold;">{primerSemana}</span><br>
                                <span style="color:{colorLetraPrimerSemana};font-size: 20px;font-weight: bold;">{pulse1SemanaPromedio}</span>
                            </div>
                        """,
                        unsafe_allow_html=True
                    )

            with st.container():
                st.markdown(
                    f"""
                        <div style="padding-block: 10px; border-radius: 10px; text-align: center; margin-bottom: 10px; background-color: {colorPrimerMes};">
                            <span style="color:{colorLetraPrimerMes}; font-size: 16px;font-weight: bold;">{primerMes}</span><br>
                            <span style="color:{colorLetraPrimerMes};font-size: 20px; font-weight: bold;">{primerMesPromedio}</span>
                        </div>
                    """,
                    unsafe_allow_html=True
                )
            with st.container():
                st.markdown(
                    f"""
                        <div style="padding-block: 10px; border-radius: 10px; text-align: center; margin-bottom: 10px; background-color: {colorAprendizCierrePrimerCiclo};">
                            <span style="color: {colorLetraPrimerCierre}; font-size: 16px;font-weight: bold;">{primerCierre}</span><br>
                            <span style="color: {colorLetraPrimerCierre};font-size: 20px; font-weight: bold;">{aprendizCierrePrimerCicloPromedio}</span>
                        </div>
                    """,
                    unsafe_allow_html=True
                )
        with col2:
            with st.container():
                st.markdown(
                    f"""
                        <div style="padding-block: 10px; border-radius: 10px; text-align: center; margin-bottom: 10px; background-color: {colorCambioArea};">
                            <span style="color:{colorLetraCambioArea};font-size: 16px;font-weight: bold;">{cambioArea}</span><br>
                            <span style="color:{colorLetraCambioArea};font-size: 20px; font-weight: bold;">{cambioAreaPromedio}</span>
                        </div>
                    """,
                    unsafe_allow_html=True
                )
            with st.container():
                st.markdown(
                    f"""
                        <div style="padding-block: 10px; border-radius: 10px; text-align: center; margin-bottom: 10px; background-color: {colorCuartoMes};">
                            <span style="color:{colorLetraCuartoMes}; font-size: 16px;font-weight: bold;">{cuartoMes}</span><br>
                            <span style="color:{colorLetraCuartoMes};font-size: 20px;font-weight: bold;">{cuartoMesPromedio}</span>
                        </div>
                    """,
                    unsafe_allow_html=True
                )
            with st.container():
                st.markdown(
                    f"""
                        <div style="padding-block: 10px; border-radius: 10px; text-align: center; margin-bottom: 10px; background-color: {colorAprendizCierreSegundoCiclo};">
                            <span style="color: {colorLetraSegundoCierre}; font-size: 16px;font-weight: bold;">{segundoCierre}</span><br>
                            <span style="color: {colorLetraSegundoCierre}; font-size: 20px;font-weight: bold;">{aprendizCierreSegundoCicloPromedio}</span>
                        </div>
                    """,
                    unsafe_allow_html=True
                )

with referencia:
    with st.container():
        st.subheader(semaforoFeedback)
        st.markdown(
            f"""
            <div style="background-color:{aquamarine}; border-radius: 10px; padding: 10px; text-align: center;">
                <span style="color: white; font-size: 16px; font-weight: bold;">{resultadoVerde}</span></br>
                <span style="color: white; font-size: 12px;">{resultadoVerdeDetalle}</span>
            </div></br>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div style="background-color:{azul};; border-radius: 10px; padding: 10px; text-align: center;">
                <span style="color: white; font-size: 16px; font-weight: bold;">{resultadoAmarillo}</span></br>
                <span style="color: white; font-size: 12px;">{resultadoAmarilloDetalle}</span>
            </div></br>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div style="background-color: {amarillo}; border-radius: 10px; padding: 10px; text-align: center;">
                <span style="color: {azul}; font-size: 16px; font-weight: bold;">{resultadoAzul}</span></br>
                <span style="color:{azul}; font-size: 12px;">{resultadoAzulDetalle}</span></br>
            </div></br>
            """,
            unsafe_allow_html=True,
        )
with st.expander(detalleFeedbackTitle):
    with st.container():
        tabs = st.tabs(feedback_types)
        with tabs[0]:
            if feedbackPulseDf is not None and not feedbackPulseDf.empty:
                st.dataframe(feedbackPulseDf, hide_index="true")
            else:
                st.write(noDatosDisponibles)
        with tabs[1]:
            if feedbackCambioAreaDf is not None and not feedbackCambioAreaDf.empty:
                st.dataframe(feedbackCambioAreaDf, hide_index="true")
            else:
                st.write(noDatosDisponibles)
        with tabs[2]:
            if feedback1MesDf is not None and not feedback1MesDf.empty:
                st.dataframe(feedback1MesDf, hide_index="true")
            else:
                st.write(noDatosDisponibles)
        with tabs[3]:
            if feedback4MesDf is not None and not feedback4MesDf.empty:
                st.dataframe(feedback4MesDf, hide_index="true")
            else:
                st.write(noDatosDisponibles)
        with tabs[4]:
            if feedbackAprendizPrimerCierreDf is not None and not feedbackAprendizPrimerCierreDf.empty:
                st.dataframe(feedbackAprendizPrimerCierreDf, hide_index="true")
            else:
                st.write(noDatosDisponibles)
        with tabs[5]:
            if feedbackAprendizSegundoCierreDf is not None and not feedbackAprendizSegundoCierreDf.empty:
                st.dataframe(feedbackAprendizSegundoCierreDf, hide_index="true")
            else:
                st.write(noDatosDisponibles)

def getCambioArea():
    cambioArea = get_sheets(connectionUsuarios, [cambioAreaSheet])
    return cambioArea[0]
with st.container():
    active_candidates_this_year = active_candidates[
        pd.to_datetime(active_candidates[columnaFechaInicio], dayfirst=True) > pd.to_datetime(anioActual, dayfirst=True)
    ]
    st.subheader('**Estado Respuestas**') 
    tabs = st.tabs(feedback_types)
    for i, feedback in enumerate(feedback_types):
        with tabs[i]:
            st.write('')
            graficosRespuestas, respuestasRecibidas, respuestasPendientes, respuestasSinResponder, = st.columns([1,2,2,2])
            if i == 0:
                response_data, candidatos_feedback_inprogress = calcularEstadoRespuestas(active_candidates_this_year, columnaEnvio1Semana, hoy, feedbackPulseDf, columnaCorreoCandidato)
            if i == 1:
                cambioAreaDf = getCambioArea()
                cambioAreaDFFiltrado = cambioAreaDf[cambioAreaDf[columnaCorreoCandidato].isin(active_candidates_this_year[columnaCorreoCandidato])]
                cambioAreaDFFiltrado = cambioAreaDFFiltrado[
                (cambioAreaDFFiltrado[columnaFPDualFCT] == valorFPDUALINT) &
                (cambioAreaDFFiltrado[columnaFechaInicio].notna()) &
                (cambioAreaDFFiltrado[columnaFechaInicio] != '')
                ]

                # Crear 8 subtabs
                subtabs = st.tabs(cambioArea_types)
                for j, subtab in enumerate(subtabs):
                    with subtab:
                        response_data, candidatos_feedback_inprogress = calcularEstadoRespuestaCambioArea(
                            cambioAreaDFFiltrado, hoy, feedbackCambioAreaDf, columnaCorreoCandidato, j
                        )

                        graficosRespuestas, respuestasRecibidas, respuestasPendientes, respuestasSinResponder = st.columns([1, 2, 2, 2])

                        with graficosRespuestas:
                            percentage = response_data['% Respuestas']
                            if percentage < 40:
                                color = 'yellow'
                            elif 40 <= percentage <= 70:
                                color = 'blue'
                            else:
                                color = 'green'
                            chart = create_donut_chart(percentage, "Respuestas", color)
                            st.altair_chart(chart, use_container_width=True)

                        with respuestasPendientes: 
                            st.markdown(
                                f"""
                                <div style="display: flex; justify-content: center; align-items: center; text-align: center;padding-top:30px">
                                    <span style="font-size: 24px; font-weight: bold; color: {aquamarine}; margin-right: 8px;">{response_data['Feedback Enviado']}</span>
                                    <span style="color:  {azul}; font-size: 24px; font-weight: bold;">Feedback Enviados</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with respuestasRecibidas: 
                            st.markdown(
                                f"""
                                <div style="display: flex; justify-content: center; align-items: center; text-align: center;padding-top:30px">
                                    <span style="font-size: 24px; font-weight: bold; color: {aquamarine}; margin-right: 8px;">{response_data['Respuestas Recibidas']}</span>
                                    <span style="color: {azul}; font-size: 24px; font-weight: bold;">Respuestas Recibidas</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with respuestasSinResponder: 
                            st.markdown(
                                f"""
                                <div style="display: flex; justify-content: center; align-items: center; text-align: center;padding-top:30px">
                                    <span style="font-size: 24px; font-weight: bold; color: {aquamarine}; margin-right: 8px;">{response_data['Feedback Sin responder']}</span>
                                    <span style="color:  {azul}; font-size: 24px; font-weight: bold;">Feedback Sin responder</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        with st.expander("Detalle Feedbacks"):
                            if candidatos_feedback_inprogress is not None and not candidatos_feedback_inprogress.empty:
                                st.dataframe(getColumns(candidatos_feedback_inprogress,[columnaCandidatos, columnaCorreoCandidato, 'Feedback Respondido']))
                            else:
                                st.write(noDatosDisponibles)
            if i == 2:
                response_data , candidatos_feedback_inprogress= calcularEstadoRespuestas(active_candidates_this_year, columnaEnvio1Mes, hoy, feedback1MesDf, columnaCorreoCandidato)
            if i == 3:
                response_data , candidatos_feedback_inprogress= calcularEstadoRespuestas(active_candidates_this_year, columnaEnvio1Mes, hoy, feedback4MesDf, columnaCorreoCandidato)
            if i == 4:
                response_data, candidatos_feedback_inprogress = calcularEstadoRespuestas(active_candidates_this_year, columnaEnvio1Cierre, hoy, feedbackAprendizPrimerCierreDf, columnaCorreoCandidato)
            if i == 5:
                response_data , candidatos_feedback_inprogress= calcularEstadoRespuestas(active_candidates_this_year, columnaEnvio2Cierre, hoy, feedbackAprendizSegundoCierreDf, columnaCorreoCandidato)
            if i != 1:
                with graficosRespuestas:
                    percentage = response_data['% Respuestas']
                    if percentage < 40:
                        color = 'blue'
                    elif 40 <= percentage <= 70:
                        color = 'yellow'
                    else:
                        color = 'green'
                    chart = create_donut_chart(response_data['% Respuestas'], "Respuestas", color)
                    st.altair_chart(chart, use_container_width=True)
                with respuestasPendientes: 
                    st.markdown(
                        f"""
                        <div style="display: flex; justify-content: center; align-items: center; text-align: center;padding-top:30px">
                            <span style="font-size: 24px; font-weight: bold; color: {aquamarine}; margin-right: 8px;">{response_data['Feedback Enviado']}</span>
                            <span style="color: {azul}; font-size: 22px; font-weight: bold;">Feedback Enviados</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with respuestasRecibidas: 
                    st.markdown(
                        f"""
                        <div style="display: flex; justify-content: center; align-items: center; text-align: center;padding-top:30px">
                            <span style="font-size: 24px; font-weight: bold; color: {aquamarine}; margin-right: 8px;">{response_data['Respuestas Recibidas']}</span>
                            <span style="color: {azul}; font-size: 22px; font-weight: bold;">Respuestas Recibidas</span>
                            
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with respuestasSinResponder: 
                    st.markdown(
                        f"""
                        <div style="display: flex; justify-content: center; align-items: center; text-align: center;padding-top:30px">
                            <span style="font-size: 24px; font-weight: bold; color: {aquamarine}; margin-right: 8px;">{response_data['Feedback Sin responder']}</span>
                            <span style="color:  {azul}; font-size: 22px; font-weight: bold;">Feedback Sin responder</span>
                            
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with st.expander("Detalle Feedback"):
                        if candidatos_feedback_inprogress is not None and not candidatos_feedback_inprogress.empty:
                            st.dataframe(getColumns(candidatos_feedback_inprogress,[columnaCandidatos, columnaCorreoCandidato, 'Feedback Respondido']))
                        else:
                            st.write(noDatosDisponibles)
    

st.divider()
with st.container():
    st.header('**¿Cómo se distribuyen mis aprendices?**')
    st.write("")
#filter containers
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    with st.container():
        programa = col1.selectbox("**TIPO DE PROGRAMA**", options=["Todos"] + df[topFilters[3]].unique().tolist())
    with st.container():
        candidato = col2.selectbox("**APRENDIZ**", options=["Todos"] + df[topFilters[1]].unique().tolist())
    with st.container():
        hotel = col3.selectbox(f"**{topFilters[2]}**", options=["Todos"] + df[topFilters[2]].unique().tolist())
    with st.container():
        fecha_inicio = col4.date_input(f"**FECHA INICIO**", value=pd.to_datetime('01/01/2024'))


# Filter DataFrame based on selected values
filtered_df = df[
    ((df[topFilters[1]] == candidato) | (candidato == "Todos")) &
    ((df[topFilters[2]] == hotel) | (hotel == "Todos")) &
    (df[topFilters[0]] >= pd.to_datetime(fecha_inicio)) &  
    ((df[topFilters[3]] == programa) | (programa == "Todos"))
]
finalizado, baja,active_count, bajaCount, finalizadoCount,total_statuses,pdt_iniciado_count = calcularPorcentajesStatus(filtered_df)
#pie chart container and aprendiz data
graficos = [columnaPosicion,columnaHotel,columnaEstudios]
st.subheader("")
# Layout containers
totalAprendices,totalPdtInicio,containerActivos, containerBajas,containerBajasCantidad, containerFinalizados,containerFinalizadosCant = st.columns(7)
with totalAprendices:
    st.markdown(
        f"<div style='text-align: center; color: {azul}; font-size: 16px;font-weight: bold;'>Total Aprendices</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="background-color: {aquamarine}; padding: 10px; border-radius: 50%; text-align: center; margin-bottom: 10px; width: 100px; height: 100px; line-height: 80px; margin: 0 auto;">
            <span style="color: #FECA1D; font-size: 24px; font-weight: bold;">{total_statuses}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with totalPdtInicio:
    st.markdown(
        f"<div style='text-align: center; color: {azul}; font-size: 16px;font-weight: bold;'>Total PDT Inicio</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="background-color: {aquamarine}; padding: 10px; border-radius: 50%; text-align: center; margin-bottom: 10px; width: 100px; height: 100px; line-height: 80px; margin: 0 auto;">
            <span style="color: #FECA1D; font-size: 24px; font-weight: bold;">{pdt_iniciado_count}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with containerActivos:
    st.markdown(
        f"<div style='text-align: center; color: {azul}; font-size: 16px;font-weight: bold;'>Aprendices Activos</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="background-color: {azul}; padding: 10px; border-radius: 50%; text-align: center; margin-bottom: 10px; width: 100px; height: 100px; line-height: 80px; margin: 0 auto;">
            <span style="color: #FECA1D; font-size: 24px; font-weight: bold;">{active_count}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
# Bajas Card
with containerBajas:
    st.markdown(
        f"<div style='text-align: center; color: {azul}; font-size: 16px; font-weight: bold;'>Bajas %</div>",
        unsafe_allow_html=True,
    )
    if baja < 40:
        color = 'yellow'
    elif 40 <= baja <= 70:
        color = 'blue'
    else:
        color = 'green'
    baja_chart = create_donut_chart(baja, "Bajas", color)
    st.altair_chart(baja_chart, use_container_width=True)
with containerBajasCantidad:
        st.markdown(
            f"<div style='text-align: center; color: {azul}; font-size: 16px;font-weight: bold;'>Cantidad Bajas</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div style="background-color: {azul}; padding: 10px; border-radius: 50%; text-align: center; margin-bottom: 10px; width: 100px; height: 100px; line-height: 80px; margin: 0 auto;">
                <span style="color: #FECA1D; font-size: 24px; font-weight: bold;">{bajaCount}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
# Finalizados Card
with containerFinalizados:
    st.markdown("<div style='text-align: center;font-weight: bold;'>Finalizados %</div>", unsafe_allow_html=True)
    # Use columns to place the donut chart and "Cantidad" side-by-side
    if finalizado < 40:
        colorFin = 'yellow'
    elif 40 <= finalizado <= 70:
        colorFin = 'blue'
    else:
        colorFin = 'green'
    finalizado_chart = create_donut_chart(finalizado, "Finalizados", colorFin)
    st.altair_chart(finalizado_chart, use_container_width=True)
with containerFinalizadosCant:
    st.markdown(
        f"<div style='text-align: center; color: {azul}; font-size: 16px;font-weight: bold;'>Cantidad Finalizados</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="background-color: {azul}; padding: 10px; border-radius: 50%; text-align: center; margin-bottom: 10px; width: 100px; height: 100px; line-height: 80px; margin: 0 auto;">
            <span style="color: #FECA1D; font-size: 24px; font-weight: bold;">{finalizadoCount}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.subheader('**Gráficos**')
custom_colors = [aquamarine, amarillo, azul, orange] 
chartHotel,chartDepto, chartEstudio  = st.columns(3)
fig_size = (4, 4)

with chartHotel:
    fig2, ax2 = plt.subplots(figsize=fig_size, facecolor='#F0F0F0')  
    filtered_df[graficos[1]].value_counts().plot.pie(autopct='%1.1f%%', ax=ax2, colors=custom_colors,startangle=90)
    ax2.set_ylabel('')
    ax2.set_title(
    graficos[1],
    fontdict={'fontsize': 14, 'fontweight': 'bold','color': azul}  # Customize size and weight
)
    ax2.set_aspect('equal')
    st.pyplot(fig2)
with chartDepto:
    fig1, ax1 = plt.subplots(figsize=fig_size, facecolor='#F0F0F0')  
    filtered_df[graficos[0]].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1, colors=custom_colors,startangle=90)
    ax1.set_ylabel('')
    ax1.set_title(
    graficos[0],
    fontdict={'fontsize': 14, 'fontweight': 'bold','color': azul} 
)
    ax1.set_aspect('equal')
    st.pyplot(fig1)
with chartEstudio:
    fig3, ax3 = plt.subplots(figsize=fig_size, facecolor='#F0F0F0')  # Set the figure background color
    filtered_df[graficos[2]].value_counts().plot.pie(
        autopct='%1.1f%%', ax=ax3, colors=custom_colors, startangle=90
    )
    ax3.set_ylabel('')
    ax3.set_title(
    graficos[2],
    fontdict={'fontsize': 14, 'fontweight': 'bold','color': azul} 
)
    ax3.set_aspect('equal')
    st.pyplot(fig3)

st.divider()
#rotacion
columnaMesesActivos="Meses Activos"
columnaDeptoDestino="Departamento de Destino"
columnaDeptoOrigen="Departamento de Origen"
columnaHotelDestino="Hotel destino"
columnaNombre="Nombre"
columnaFechaInicioRotacion="Fecha de Inicio"
columnaEmailAprendiz="MAIL APRENDIZ"

def getRotationInfo():
    rotacion = get_sheets(connectionUsuarios, [rotationSheet])
    filters = {filtrosTutor[1]: [st.session_state.username]}
    rotacionDelTutor = filter_dataframeToUpper(rotacion[0], filters)
    return rotacionDelTutor

#donde estan mis aprendices
with st.container():
    st.header(dondeEstanMisAprendices)
    graficoHotel, tablaAprendicesHoy  = st.columns([1.6,1.4])
    rotacion = pd.DataFrame() 

    with graficoHotel:
        if active_candidates is not None and not active_candidates.empty:
            rotacionUnfiltered= getRotationInfo()

            rotacionUnfiltered[columnaEmailAprendiz] = rotacionUnfiltered[columnaEmailAprendiz].str.upper()
            active_candidates[columnaCorreoCandidato] = active_candidates[columnaCorreoCandidato].str.upper()

            rotacion = rotacionUnfiltered[
                rotacionUnfiltered[columnaEmailAprendiz].isin(active_candidates[columnaCorreoCandidato])
            ]
            rotacion[columnaMesesActivos] = pd.to_datetime(rotacion[columnaMesesActivos], format='%d/%m/%Y')
            # Filtrar datos para el próximo mes en adelante y agrupar por hotel, mes y departament
            mes_actual = hoy.replace(day=1)
            prox_mes = hoy.replace(day=1) + timedelta(days=31)
            prox_mes = prox_mes.replace(day=1)  # Primer día del próximo mes
            dfRot = rotacion[rotacion[columnaMesesActivos] >= mes_actual]
            # Crear una columna para el mes (año-mes) y agrupar
            dfRot["Mes"] = dfRot[columnaMesesActivos].dt.to_period("M").astype(str)
            dfRot[columnaDeptoDestino] = dfRot[columnaDeptoDestino].str.strip().str.title()
            dfRot = dfRot.drop_duplicates(subset=[columnaNombre, columnaDeptoOrigen, columnaDeptoDestino, columnaMesesActivos])
            # Agrupar por hotel, mes y departamento destino
            df_grouped = dfRot.groupby([columnaHotelDestino, "Mes", columnaDeptoDestino]).size().reset_index(name="Cantidad")

            # Obtener los próximos 12 meses como períodos
            meses_futuros = pd.date_range(prox_mes, periods=12, freq="MS").strftime("%Y-%m").tolist()
            color_map = generate_color_map(dfRot, columnaDeptoDestino)
            # Crear gráficos individuales para cada hotel
            hoteles = dfRot[columnaHotelDestino].unique()
            carousel_items = []
            for hotel in hoteles:
                # Filtrar los datos del hotel específico
                hotel_data = df_grouped[df_grouped[columnaHotelDestino] == hotel]
                hotel_data["Mes"] = pd.Categorical(hotel_data["Mes"], categories=meses_futuros, ordered=True)
                # Crear gráfico de barras
                fig = px.bar(
                    hotel_data,
                    x="Mes",
                    y="Cantidad",
                    color=columnaDeptoDestino,
                    color_discrete_map=color_map,
                    category_orders={"Mes": meses_futuros},  # Ordenar los meses en el gráfico
                    title=f"Aprendices por Departamento en {hotel} (Próximos 12 meses)",
                    labels={"Cantidad": "Número de Candidatos", "Mes": "Mes", "Departamento de Destino": "Departamento"},
                    text="Cantidad"
                )
                
                fig.update_traces(textposition="outside")
                fig.update_layout(xaxis=dict(type='category'))
                    # Save the figure as an image
                fig.write_image(f"{hotel}.png")

                # Add the slide to the carousel items
                carousel_items.append({
                    "title": "",
                    "text": "",
                    "img": f"{hotel}.png"
                })
            # Display the carousel
            carousel(items=carousel_items)

        else:
            st.write(noDatosDisponibles)

    mes_actual = hoy.replace(day=1)
    prox_mes = hoy.replace(day=1) + timedelta(days=31)
    prox_mes = prox_mes.replace(day=1)  # Primer día del próximo mes
    if rotacion is not None and not rotacion.empty:
        rotacion = rotacion[rotacion[columnaMesesActivos] >= mes_actual]
        result_df = rotacion.groupby(
        ["Nombre", "Departamento de Destino", "Hotel destino", "Fecha de Inicio"]
            ).agg(
                {
                    "Meses Activos": lambda x: ", ".join(sorted(x.astype(str).unique()))
                }
            ).reset_index()
        result_df= result_df.sort_values(by=columnaFechaInicioRotacion,ascending=[False])
        with tablaAprendicesHoy:
            col1, col2 = st.columns(2)
            with st.container():
                hotel_options = sorted(result_df[columnaHotelDestino].unique().tolist())
                hotel = col1.selectbox(f"**{columnaHotelDestino}**", options=["Todos"] + hotel_options,key='hotelDestino')
            with st.container():
                depto_options = sorted(result_df[columnaDeptoDestino].unique().tolist())
                depto = col2.selectbox(f"**{columnaDeptoDestino}**", options=["Todos"] + depto_options,key='deptoDestino')
        # Filter DataFrame based on selected values
            filtered_df = result_df[
                ((result_df[columnaHotelDestino] == hotel) | (hotel == "Todos")) &
                ((result_df[columnaDeptoDestino] == depto) | (depto == "Todos"))]
            if filtered_df is not None and not filtered_df.empty:
                st.dataframe(filtered_df, hide_index="true")
            else:
                st.write(noDatosDisponibles)
      

