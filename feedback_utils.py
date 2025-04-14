from data_utils import getColumns
import streamlit as st
import json
import pandas as pd
with open('content/formularioPulse1Semana.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

def getFeedbackPulse1Semana(feedback):
    dfiltered = getColumns(feedback, [quiz_data["text_form"]["questions"][1]["question"],quiz_data["text_form"]["questions"][2]["question"],quiz_data["text_form"]["questions"][4]["question"]])
    feedback_mapping = {
    "Genial 😊": 4,
    "Bien 👍": 3,
    "Regular 😐": 2,
    "Me ha costado 😕": 1,
    "Sí, me sirvió bastante": 3,
    "Estuvo bien, pero podría haber sido más completa": 2,
    "Me pareció que faltaba información": 1,
    "Sí, totalmente": 3,
    "Más o menos": 2,
    "No mucho": 1,
}
    max_ponderacion = 4 #maximo valor de la respuesta
    df_mapped = dfiltered.map(lambda x: feedback_mapping.get(x, 0))

    # Step 3: Calculate averages
    average_scores = df_mapped.mean()
    
    promedio_escalado = (average_scores/max_ponderacion)*10
    return round(promedio_escalado.mean(), 2)


with open('content/formulario_cambio_area.json', 'r', encoding='utf-8') as f:
    quiz_data_cambio_area = json.load(f)

def getFeedbackPromedioCambioArea(feedback):
    dfiltered = getColumns(feedback, [quiz_data_cambio_area["text_form"]["questions"][2]["question"],quiz_data_cambio_area["text_form"]["questions"][3]["question"]])
    feedback_mapping = {
    "Súper cómodo/a 😊": 4,
    "Bien": 3,
    "Me costó adaptarme": 2,
    "No me sentí cómodo/a": 1,
    4:4,
    3:3,
    2:2,
    1:1
}
    max_ponderacion = 4 #maximo valor de la respuesta
    df_mapped = dfiltered.map(lambda x: feedback_mapping.get(x, 0))
    # Step 3: Calculate averages
    average_scores = df_mapped.mean()
    
    promedio_escalado = (average_scores/max_ponderacion)*10
    return round(promedio_escalado.mean(), 2)

with open('content/formulario_primer_mes.json', 'r', encoding='utf-8') as f:
    quiz_data_primer_mes = json.load(f)

def getFeedbackPromedioPrimerMes(feedback):
    dfiltered = getColumns(feedback,[quiz_data_primer_mes["text_form"]["questions"][1]["question"],quiz_data_primer_mes["text_form"]["questions"][2]["question"],quiz_data_primer_mes["text_form"]["questions"][3]["question"],quiz_data_primer_mes["text_form"]["questions"][4]["question"],quiz_data_primer_mes["text_form"]["questions"][5]["question"]])
    feedback_mapping = {
    "Súper bien": 4,
    "Bien": 3,
    "Un poco perdido/a": 2,
    "No me sentí cómodo/a": 1,
    4:4,
    3:3,
    2:2,
    1:1
}
    max_ponderacion = 4 #maximo valor de la respuesta
    df_mapped = dfiltered.map(lambda x: feedback_mapping.get(x, 0))
    # Step 3: Calculate averages
    average_scores = df_mapped.mean()
    
    promedio_escalado = (average_scores/max_ponderacion)*10
    return round(promedio_escalado.mean(), 2)

with open('content/formulario_cuarto_mes.json', 'r', encoding='utf-8') as f:
    quiz_data_cuarto_mes = json.load(f)

def getFeedbackPromedioCuartoMes(feedback):
    dfiltered = getColumns(feedback,[quiz_data_cuarto_mes["text_form"]["questions"][1]["question"],quiz_data_cuarto_mes["text_form"]["questions"][2]["question"],quiz_data_cuarto_mes["text_form"]["questions"][3]["question"]])
    feedback_mapping = {
    4:4,
    3:3,
    2:2,
    1:1
}
    max_ponderacion = 4 #maximo valor de la respuesta
    df_mapped = dfiltered.map(lambda x: feedback_mapping.get(x, 0))
    # Step 3: Calculate averages
    average_scores = df_mapped.mean()
    
    promedio_escalado = (average_scores/max_ponderacion)*10
    return round(promedio_escalado.mean(), 2)

with open('content/formulario_aprendiz_cierre_primer_ciclo.json', 'r', encoding='utf-8') as f:
    quiz_data_aprendiz_cierre_primer_ciclo = json.load(f)

def getFeedbackPromedioAprendizCierrePrimerCiclo(feedback):
    dfiltered = getColumns(feedback,[quiz_data_aprendiz_cierre_primer_ciclo["text_form"]["questions"][1]["question"],quiz_data_aprendiz_cierre_primer_ciclo["text_form"]["questions"][2]["question"],quiz_data_aprendiz_cierre_primer_ciclo["text_form"]["questions"][4]["question"],quiz_data_aprendiz_cierre_primer_ciclo["text_form"]["questions"][5]["question"]])
    feedback_mapping = {
        "Sí, estuvieron súper presentes":3,
        "Sí, aunque me gustaría haber tenido más apoyo":2,
        "Tuve que resolver varias cosas por mi cuenta":1,
        4:4,
        3:3,
        2:2,
        1:1
    }
    max_ponderacion = 4 #maximo valor de la respuesta
    df_mapped = dfiltered.map(lambda x: feedback_mapping.get(x, 0))
    # Step 3: Calculate averages
    average_scores = df_mapped.mean()
    
    promedio_escalado = (average_scores/max_ponderacion)*10
    return round(promedio_escalado.mean(), 2)

with open('content/formulario_aprendiz_cierre_segundo_ciclo.json', 'r', encoding='utf-8') as f:
    quiz_data_aprendiz_cierre_segundo_ciclo = json.load(f)

def getFeedbackPromedioAprendizCierreSegundoCiclo(feedback):
    dfiltered = getColumns(feedback,[quiz_data_aprendiz_cierre_segundo_ciclo["text_form"]["questions"][1]["question"],quiz_data_aprendiz_cierre_segundo_ciclo["text_form"]["questions"][2]["question"],quiz_data_aprendiz_cierre_segundo_ciclo["text_form"]["questions"][3]["question"],quiz_data_aprendiz_cierre_segundo_ciclo["text_form"]["questions"][9]["question"],quiz_data_aprendiz_cierre_segundo_ciclo["text_form"]["questions"][13]["question"]])
    feedback_mapping = {
        "Sí, estuvieron súper presentes y me ayudaron en todo":3,
        "Sí, aunque me gustaría haber tenido más apoyo":2,
        "No tanto, tuve que resolver varias cosas por mi cuenta":1,
        4:4,
        3:3,
        2:2,
        1:1,
        5:5,
        6:6,
        7:7,
        8:8,
        9:9,
        10:10
    }
    max_ponderacion = 4 #maximo valor de la respuesta
    df_mapped = dfiltered.map(lambda x: feedback_mapping.get(x, 0))
    # Step 3: Calculate averages
    average_scores = df_mapped.mean()
    
    promedio_escalado = (average_scores/max_ponderacion)*10
    return round(promedio_escalado.mean(), 2)

columnaFechaInicio='FECHA INICIO real'
cambioArea_types = ['Envío 30 días', 'Envío 60 días', 'Envío 90 días', 'Envío 120 días','Envío 150 días','Envío 180 días','Envío 300 días','Envío 330 días'] 
def calcularEstadoRespuestaCambioArea(cambioDeAreaDF, hoy, feedbackCambioAreaDf ,columnaCorreoCandidato, tipo):
    in_feedback_count=0
    total_candidates=0
    percentage_in_feedback=0
    not_in_feedback_count=0
    candidatos_feedback_inprogress=None
    cambioDeAreaDF = cambioDeAreaDF[
    (cambioDeAreaDF[cambioArea_types[tipo]].notna()) &
    (cambioDeAreaDF[cambioArea_types[tipo]] != '')
]

    if cambioDeAreaDF is not None and not cambioDeAreaDF.empty: 
            cambioDeAreaDF[cambioArea_types[tipo]] = pd.to_datetime(cambioDeAreaDF[cambioArea_types[tipo]], dayfirst=True,errors='coerce')
            candidatos_feedback_inprogress = cambioDeAreaDF[cambioDeAreaDF[cambioArea_types[tipo]] < hoy]
            if candidatos_feedback_inprogress is not None and not candidatos_feedback_inprogress.empty: 
                feedback_emails = feedbackCambioAreaDf['Email'].unique()
                feedback_emails_normalized = [email.lower() for email in feedback_emails]

                candidatos_feedback_inprogress['Normalized Email'] = candidatos_feedback_inprogress[columnaCorreoCandidato].str.lower()
                candidatos_feedback_inprogress['Feedback Respondido'] = candidatos_feedback_inprogress['Normalized Email'].isin(feedback_emails_normalized)
                candidatos_feedback_inprogress.drop(columns=['Normalized Email'], inplace=True)

                total_candidates = len(candidatos_feedback_inprogress)
                in_feedback_count = candidatos_feedback_inprogress['Feedback Respondido'].sum()
                not_in_feedback_count = total_candidates - in_feedback_count
                percentage_in_feedback = (in_feedback_count / total_candidates) * 100 if total_candidates > 0 else 0

            results = {
                'Respuestas Recibidas': in_feedback_count,
                'Feedback Enviado': total_candidates,
                '% Respuestas': round(percentage_in_feedback, 2),
                'Feedback Sin responder': not_in_feedback_count
            }
    else:
        results = {
            'Respuestas Recibidas': in_feedback_count,
            'Feedback Enviado': total_candidates,
            '% Respuestas': round(percentage_in_feedback, 2),
            'Feedback Sin responder': not_in_feedback_count
        }
    return results,candidatos_feedback_inprogress

def calcularEstadoRespuestas(active_candidates,columnaEnvio1Feedback,hoy, feedbackPulseDf,columnaCorreoCandidato ):
    in_feedback_count=0
    total_candidates=0
    percentage_in_feedback=0
    not_in_feedback_count=0
    candidatos_feedback_inprogress=None
    if feedbackPulseDf is not None and not feedbackPulseDf.empty:
        active_candidates[columnaEnvio1Feedback] = pd.to_datetime(active_candidates[columnaEnvio1Feedback], format='%d/%m/%Y')
        candidatos_feedback_inprogress = active_candidates[active_candidates[columnaEnvio1Feedback] < hoy]
        feedback_emails = feedbackPulseDf['Email'].unique()
        feedback_emails_normalized = [email.lower() for email in feedback_emails]

        candidatos_feedback_inprogress['Normalized Email'] = candidatos_feedback_inprogress[columnaCorreoCandidato].str.lower()
        candidatos_feedback_inprogress['Feedback Respondido'] = candidatos_feedback_inprogress['Normalized Email'].isin(feedback_emails_normalized)

        # Drop the temporary normalized email column (optional)
        candidatos_feedback_inprogress.drop(columns=['Normalized Email'], inplace=True)

        total_candidates = len(candidatos_feedback_inprogress)
        in_feedback_count = candidatos_feedback_inprogress['Feedback Respondido'].sum()
        not_in_feedback_count = total_candidates - in_feedback_count
        percentage_in_feedback = (in_feedback_count / total_candidates) * 100 if total_candidates > 0 else 0

        results = {
            'Respuestas Recibidas': in_feedback_count,
            'Feedback Enviado': total_candidates,
            '% Respuestas': round(percentage_in_feedback, 2),
            'Feedback Sin responder': not_in_feedback_count
        }
    else:
        results = {
            'Respuestas Recibidas': in_feedback_count,
            'Feedback Enviado': total_candidates,
            '% Respuestas': round(percentage_in_feedback, 2),
            'Feedback Sin responder': not_in_feedback_count
        }
    return results,candidatos_feedback_inprogress