import os
import sqlite3
import streamlit as st
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.errors import HttpError

# Define os escopos necessários para acessar o Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# ID e faixa da planilha do Google Sheets
SAMPLE_SPREADSHEET_ID = "1pHyYyhlL2QJyJ7Se0hKJIER4tjMhlfpIT1RtA1vmvis"
SAMPLE_RANGE_NAME = "dados!A1:Z10000"

# Função para autenticar e obter credenciais
def get_google_sheets_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        return service
    except HttpError as error:
        st.error(f"An error occurred: {error}")
        return None

# Função para buscar dados da tabela pagamentos no SQLite
def fetch_data_from_sqlite():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pagamentos")
    data = cursor.fetchall()
    conn.close()
    return data

# Função para salvar dados no Google Sheets
def backup_to_google_sheets(data):
    service = get_google_sheets_service()
    if service:
        sheet = service.spreadsheets()
        try:
            # Convertendo os dados para o formato que o Google Sheets espera
            values = [list(row) for row in data]
            body = {
                "values": values
            }
            # Salvando os dados no Google Sheets
            sheet.values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=SAMPLE_RANGE_NAME,
                valueInputOption="RAW",
                body=body
            ).execute()
            st.success("Backup realizado com sucesso no Google Sheets!")
        except HttpError as error:
            st.error(f"Erro ao enviar dados para o Google Sheets: {error}")

# Interface do Streamlit
st.title("Backup de Pagamentos para Google Sheets")

if st.button("Realizar Backup"):
    data = fetch_data_from_sqlite()
    if data:
        backup_to_google_sheets(data)
    else:
        st.warning("Não há dados na tabela 'pagamentos' para fazer backup.")
