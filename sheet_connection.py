import logging
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import gspread
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
logging.basicConfig(level=logging.DEBUG)

@st.cache_data(ttl=3600) # Cache the result to avoid reloading each time
def get_google_sheet(connection, sheet_id):
    """
    Connects to a Google Sheet using service account credentials and returns the sheet.
    """
    try:
        url=f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit?usp=sharing"
        conn = st.connection(connection, type=GSheetsConnection)
        df = conn.read(spreadsheet=url)  
        if df is not None and not df.empty:
             return df 
        else:
            st.error("No data found.")
            return None

    except FileNotFoundError as e:
        logging.error(f"Service account file not found: {e}")
        return None
    except gspread.exceptions.APIError as e:
        logging.error(f"Google Sheets API error: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None


@st.cache_data(ttl=3600)  # Cache the result to avoid reloading each time
def get_sheets(connection, worksheetNames):
    try:
        dfs=[]
        conn = st.connection(connection, type=GSheetsConnection)
        for worksheet_name in worksheetNames:
            df = conn.read(worksheet=worksheet_name)
            if df is not None and not df.empty:
                dfs.append(df)  
            else:
                logging.warning(f"No data found for worksheet: {worksheet_name}")
                dfs.append(None) 
        return dfs

    except FileNotFoundError as e:
        logging.error(f"Service account file not found: {e}")
        return None
    except gspread.exceptions.APIError as e:
        logging.error(f"Google Sheets API error: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None
@st.cache_data(ttl=3600)
def get_all_worksheets(connection):
    try:
        conn = st.connection(connection, type=GSheetsConnection)
        return conn

    except FileNotFoundError as e:
        logging.error(f"Service account file not found: {e}")
        return None
    except gspread.exceptions.APIError as e:
        logging.error(f"Google Sheets API error: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None

def upload_to_drive(file_name,folder_id,emailCandidato):
    credentials_info = st.secrets.connections.gcs
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    service = build('drive', 'v3', credentials=credentials)
    media = MediaFileUpload(file_name, resumable=True)
    file_metadata = {
        'name': emailCandidato,
        'parents': [folder_id]
    }

    # Upload the file
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return uploaded_file['id']