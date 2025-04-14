from variables import celeste, amarillo, aquamarine, azul, orange, teal, gris,rojo,verde
import re 
import pandas as pd
import altair as alt
from streamlit_carousel import carousel
def filter_dataframe(df, filters):
    for column, value in filters.items():
        df = df[df[column].isin(value)]
    return df

def filter_dataframeToUpper(df, filters):
    for column, value in filters.items():
        df = df[df[column].str.upper().isin(value)]
    return df

def getColumns(df, columns):
        missing_columns = [col for col in columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Columns not found in DataFrame: {missing_columns}")
        
        return df[columns]

import itertools

def generate_color_map(df, column_name):
    # Define a base list of colors to use
    base_colors = [
        aquamarine,  # Aquamarine
        amarillo,  # Yellow
        azul,  # Blue
        orange,  # Orange
        celeste,  # Light Blue
        teal,  # Teal
        gris,  # Gray
        "#9467BD"   # Purple
    ]
    
    # Get unique departments
    unique_departments = df[column_name].unique()
    
    # Cycle through colors if there are more departments than base colors
    color_cycle = itertools.cycle(base_colors)
    
    # Create a dictionary mapping each department to a color
    color_map = {dept: next(color_cycle) for dept in unique_departments}
    
    return color_map


def is_valid_email(email):
    # Simple regex for validating an email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

columnStatus = 'STATUS'
def calcularPorcentajesStatus(df):
    aprendicesStatus = getColumns(df, [columnStatus])
    total_statuses = len(aprendicesStatus)
    finalizado_count = df[columnStatus].str.lower().eq('finalizado').sum()
    pdt_iniciado_count = df[columnStatus].str.lower().eq('pdt inicio').sum()
    baja_count = df[columnStatus].str.lower().eq('baja').sum()
    activo_count = df[columnStatus].str.lower().eq('activo').sum()
    baja_pct =0
    finalizado_pct=0
    # Calcular los porcentajes
    if finalizado_count != 0:
       finalizado_pct = int((finalizado_count / total_statuses) * 100) 
    if baja_count !=0:
        baja_pct = int((baja_count / total_statuses) * 100)
    return finalizado_pct, baja_pct,activo_count, baja_count,finalizado_count,total_statuses,pdt_iniciado_count

def create_donut_chart(input_response, input_text, input_color):
    if input_color == 'blue':
        chart_color = [azul, '#cbdcfb']
    if input_color == 'yellow':
        chart_color = [amarillo, '#cbdcfb']
    if input_color == 'orange':
        chart_color = [orange, '#cbdcfb']
    if input_color == 'green':
        chart_color = [aquamarine, '#cbdcfb']
        
    source = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100-input_response, input_response]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100, 0]
    })
        
    plot = alt.Chart(source).mark_arc(innerRadius=35, cornerRadius=15).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            #domain=['A', 'B'],
                            domain=[input_text, ''],
                            # range=['#29b5e8', '#155F7A']),  # 31333F
                            range=chart_color),
                        legend=None),
    ).properties(width=120, height=120)
        
    text = plot.mark_text(align='center', color="#29b5e8", fontSize=20, fontWeight=700).encode(text=alt.value(f'{input_response} %'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=35, cornerRadius=10).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            # domain=['A', 'B'],
                            domain=[input_text, ''],
                            range=chart_color),  # 31333F
                        legend=None),
    ).properties(width=120, height=120)
    return plot_bg + plot + text

def create_events(df, columns_to_extract):
    events = []
    # Iterate over DataFrame rows
    for index, row in df.iterrows():
        # Parse dates and handle NaT values
        start_date = pd.to_datetime(row[columns_to_extract[1]], dayfirst=True)
        end_date = pd.to_datetime(row[columns_to_extract[2]], dayfirst=True)
        feedback1Semana = pd.to_datetime(row[columns_to_extract[3]], dayfirst=True)
        feedback1Mes = pd.to_datetime(row[columns_to_extract[4]], dayfirst=True)
        feedback4Mes = pd.to_datetime(row[columns_to_extract[5]], dayfirst=True)
        # Check if dates are valid and not NaT
        if pd.notna(start_date):
            start_date_str = start_date.strftime('%Y-%m-%d')
            # Create start event
            start_event = {
                "start": start_date_str,
                "title": f"Inicio {row[columns_to_extract[0]]}",
                "backgroundColor": amarillo
            }
            events.append(start_event)
        
        if pd.notna(end_date):
            end_date_str = end_date.strftime('%Y-%m-%d')
            # Create end event
            end_event = {
                "start": end_date_str,
                "title": f"Fin {row[columns_to_extract[0]]}",
                "backgroundColor": aquamarine
            }
            events.append(end_event)
        if pd.notna(feedback1Semana):
            feedback1Semana_str = feedback1Semana.strftime('%Y-%m-%d')
            # Create end event
            feedback1SemanaEvent = {
                "start": feedback1Semana_str,
                "title": f"Envio Feedback 1 Semana - {row[columns_to_extract[0]]}",
                "backgroundColor": gris
            }
            events.append(feedback1SemanaEvent)
        if pd.notna(feedback1Mes):
            feedback1Mes_str = feedback1Mes.strftime('%Y-%m-%d')
            # Create end event
            feedback1MesEvent = {
                "start": feedback1Mes_str,
                "title": f"Envio Feedback 1 Mes - {row[columns_to_extract[0]]}",
                "backgroundColor": azul
            }
            events.append(feedback1MesEvent)
        if pd.notna(feedback4Mes):
            feedback4Mes_str = feedback4Mes.strftime('%Y-%m-%d')
            # Create end event
            feedback4MesEvent = {
                "start": feedback4Mes_str,
                "title": f"Envio Feedback 4 Mes - {row[columns_to_extract[0]]}",
                "backgroundColor": orange
            }
            events.append(feedback4MesEvent)
    return events


def feedbackColor(value):
    if value == 0:
        color = "white"
        letraColor = "black"
    elif 1 <= value < 4:  # Less than 4
        color = amarillo
        letraColor = "black"
    elif 4 <= value <= 7:  # Between 4 and 7, inclusive
        color = azul
        letraColor = "white"
    else:  # Greater than 7
        color = aquamarine
        letraColor = "black"
    return color, letraColor


def crearAgenda():
    carousel_items = []  # Initialize as an empty list

    # Append items to the carousel
    carousel_items.append({
        "title": "",
        "text": "",
        "img": "./images/agenda_1_DH.png"
    })
    carousel_items.append({
        "title": "",
        "text": "",
        "img": "./images/agenda_2_DH.png"
    })
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

    carousel(items=carousel_items, container_height= 1100)
    