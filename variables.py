
import streamlit as st
import location.es as vars

#main Db
registroAprendices="1s87GZXzQuZvGix9LPSo51NnIlA8IrjEpbIgR1bOETxI"
feedbackSheets="1SkBunMV_Ij-Z2w5kyRYUVqJWly0J3EIOVhrgZaVG7kA"
agendaSheets="1OJ7tinHw7K-fx_kiK3r7pAHPXVf-PO8b0o8FDhXpGwg"
connectionGeneral="gsheets"
connectionFeedbacks="gsheets_feedback"
connectionFeedbackPerfilTutor="gsheets_feedback_perfil_tutor"
worksheetPerfilTutor="formTutor"
connectionUsuarios="usuarios"
worksheetUsuarios="Usuarios"
worksheetPulse1Semana="formularioPulse1Semana"
worksheetCambioArea="formularioCambioArea"
worksheetFormulario1Mes="formulario1Mes"
worksheetFormulario4Mes="formularioCuatroMes"
worksheetFormularioAprendizCierre1Ciclo="formularioAprendizCierre1Ciclo"
worksheetFormularioAprendizCierre2Ciclo="formularioAprendizCierre2Ciclo"
worksheetFormularioTutorCierre1Ciclo="formularioTutorCierre1Ciclo"
worksheetFormularioTutorCierre2Ciclo="formularioTutorCierre2Ciclo"
formAprendiz="formAprendiz"
rotationSheet="Rotacion"
cambioAreaSheet="Feedback_cambio_area"
anioActual='01/01/2025'
costeSheet = ""
formsSheet = ""
#branding colors 
aquamarine="#3AA597"
amarillo="#FECA1D"
azul="#002855"
orange="#FF6B35"
celeste="#007EA7"
teal="#00A6A6"
gris="#8D99AE"
verde="#08af64"
rojo="#d62828"

#login
username=vars.username
password=vars.password
forgotPassword=vars.forgotPassword
loginButton=vars.loginButton
logoutButton=vars.logoutButton
errorRedirection=vars.errorRedirection
IncorrectPassword=vars.IncorrectPassword
logoutMessage=vars.logoutMessage
loginMessage=vars.loginMessage
loginDescription=vars.loginDescription
noDatosDisponibles="No hay datos disponibles"

page_icon="./images/icon.ico"
companyIcon="./images/smallIcon.png"
title= vars.title

#comunes
tituloOrganizacion="Planifica el camino!"
tituloCalendario="Mantente al Día con los Próximos Pasos"
feedbackTitle="¿Cómo van tus aprendices?"
feedbackSubtitle="Usa sus feedbacks y reflexiones para conocer sus avances, inquietudes y seguir apoyándolos en cada etapa. Ten en cuenta los colores para tomar acciones:"
detalleFeedbackTitle="¡Accede aquí al detalle completo de sus comentarios!"
dondeEstanMisAprendices="¿En dónde se encuentran hoy mis aprendices?"
primerSemana="1° Semana"
primerMes="1° Mes"
cuartoMes="4° Mes"
primerCierre="1° Ciclo Cierre"
segundoCierre="2° Ciclo Cierre"
cambioArea="Cambio de área"
feedback_types = [primerSemana, cambioArea, primerMes, cuartoMes,primerCierre,segundoCierre]
cambioArea_types = ['30 días', '60 días', '90 días', '120 días','150 días','180 días','300 días','330 días'] 
#tutor dashboard 
preOnboardingImage="https://github.com/user-attachments/assets/7dd8d62d-b5ce-44ac-bda9-5eca1459a8b3"
onboardingImage="https://github.com/user-attachments/assets/2234162c-6c63-4ea4-9565-69206f7870fa"
seguimientoImage="https://github.com/user-attachments/assets/e55e814d-2b7c-4b7b-a8f6-e0c6927e06ca"
cierreImage="https://github.com/user-attachments/assets/c7609f53-4bb7-4b1b-8d1f-44bdbd24f379"
recursosUtiles=vars.recursosUtiles
documentacionTitle=vars.documentacionTitle
tabPreOnboarding=vars.tabPreOnboarding
tabOnboarding=vars.tabOnboarding
tabSeguimiento=vars.tabSeguimiento
tabCierre=vars.tabCierre
tabFeedback="Formularios"
referenciaColores="Recomendaciones por color:"
#menu pages
tutorDashboard=vars.tutorDashboard
aprendizDashboard=vars.aprendizDashaboard
adminRecursosTutorDashboard=vars.adminRecursosTutorDashboard
adminTutorDashboard=vars.adminTutorDashboard
preOnboardingLinks = ["Guía Exprés!", "https://drive.google.com/file/d/1pYGXJ_WRE3skOOd_tZR3Q91ofG2B0vzQ/view?usp=sharing", "Rol Tutor y Rol Aprendiz","https://drive.google.com/file/d/1pYGXJ_WRE3skOOd_tZR3Q91ofG2B0vzQ/view?usp=sharing"]
onboardingLinks = ["Manual 1: Claves para los 'Primeros días'", "https://drive.google.com/file/d/1pYGXJ_WRE3skOOd_tZR3Q91ofG2B0vzQ/view?usp=sharing"]
seguimientoLinks = ["Manual 2: Claves para el 'Cambio de área'", "https://drive.google.com/file/d/1pYGXJ_WRE3skOOd_tZR3Q91ofG2B0vzQ/view?usp=sharing","Manual 3: Claves para el 'Seguimiento' (Tutor/a c/Aprendiz)","https://drive.google.com/file/d/1pYGXJ_WRE3skOOd_tZR3Q91ofG2B0vzQ/view?usp=sharing"]
cierreLinks = ["Manual 4: Claves para el 'Cierre 1º ciclo y 2° Ciclo'", "https://drive.google.com/file/d/1pYGXJ_WRE3skOOd_tZR3Q91ofG2B0vzQ/view?usp=sharing"]
formsLinks = ["Primera Semana", "https://fpdual-demo.streamlit.app/pulse_primera_semana",
"Cambio Area","https://fpdual-demo.streamlit.app/formulario_cambio_area",
"Primer Mes", "https://fpdual-demo.streamlit.app/formulario_primer_mes",
"Cuarto Mes", "https://fpdual-demo.streamlit.app/formulario_cuarto_mes",
"Cierre 1° Ciclo","https://fpdual-demo.streamlit.app/formulario_aprendiz_cierre_primer_ciclo",
"Cierre 2° Ciclo","https://fpdual-demo.streamlit.app/formulario_aprendiz_cierre_segundo_ciclo",
"Reflexión 1° Ciclo","https://fpdual-demo.streamlit.app/formulario_tutor_cierre_primer_ciclo",
"Reflexión 2° Ciclo","https://fpdual-demo.streamlit.app/formulario_tutor_cierre_segundo_ciclo"
              ]


#admin dashboard
aprendiz_looker_url = "https://lookerstudio.google.com/embed/reporting/0007bb0d-c669-4d28-ba4d-77642dd4af63/page/XQXmD"
presupuesto_looker_url="https://lookerstudio.google.com/embed/reporting/0007bb0d-c669-4d28-ba4d-77642dd4af63/page/XQXmD"
aprendiz_2025_looker_url="https://lookerstudio.google.com/embed/reporting/0007bb0d-c669-4d28-ba4d-77642dd4af63/page/XQXmD"

#forms
folderIdAprendriz="1ipDPOh8RhBMQF6SpA9nKglcvavZKHh-E"
folderIdTutor="1qQZGjDTukHla-_pbhLeppLHxogNKSmML"
smileFacePath="https://github.com/user-attachments/assets/dd9fe972-19e1-46c0-bff6-bb2df20716ef"
rocketPath="https://github.com/user-attachments/assets/75b1a65f-6416-4366-b54e-ba3b56c49333"
camaraPath="https://github.com/user-attachments/assets/50d2c611-8a03-42c5-81da-1f6cf1820942"
autocompletarTutor="=IFERROR(VLOOKUP($A3,Base_datos!$A:$C,3,0))"
autocompletarNombre="=IFERROR(VLOOKUP($A3,Base_datos!$A:$D,4,0))"

pulse1SemanaPromedio= 'Sin Datos'
cambioAreaPromedio= 'Sin Datos'
primerMesPromedio ='Sin Datos'
cuartoMesPromedio='Sin Datos'
aprendizCierrePrimerCicloPromedio='Sin Datos'
aprendizCierreSegundoCicloPromedio='Sin Datos'
colorPulse='white'
colorCambioArea='white'
colorPrimerMes='white'
colorCuartoMes='white'
colorPrimerCierre='white'
colorSegundoCierre='white'
colorAprendizCierrePrimerCiclo='white'
colorAprendizCierreSegundoCiclo='white'

#referenciasFeedback
resultadoAzul="¡Hay oportunidades de mejora en varios puntos!"
resultadoAzulDetalle="¡Es importante que te detengas y analices con detalle el feedback para mejorar su experiencia!"
resultadoAmarillo="¡Van bien, pero hay puntos que se pueden mejorar!"
resultadoAmarilloDetalle="Revisa el feedback de tu aprendiz y ajusta lo que sea necesario para fortalecer su experiencia."
resultadoVerde="¡Todo marcha perfecto!"
resultadoVerdeDetalle="Tu aprendiz está feliz con su progreso. Reafirma sus logros y sigue celebrando sus avances."
semaforoFeedback="Semáforo de Feedback"
resultadosFeedback="Resultados de los Formularios"