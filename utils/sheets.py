import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from datetime import datetime

SPREADSHEET_ID = "1rQVCkuO1q055CLyD2VhDuZhxytH81SZGj0oo6HbAbQ8"

def get_google_sheets():
    """Initialize Google Sheets connection"""
    credentials = {
        "type": "service_account",
        "project_id": st.secrets["GSHEETS_PROJECT_ID"],
        "private_key_id": st.secrets["GSHEETS_PRIVATE_KEY_ID"],
        "private_key": st.secrets["GSHEETS_PRIVATE_KEY"].replace('\\n', '\n'),
        "client_email": st.secrets["GSHEETS_CLIENT_EMAIL"],
        "client_id": st.secrets["GSHEETS_CLIENT_ID"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": st.secrets["GSHEETS_CLIENT_X509_CERT_URL"]
    }
    
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    creds = Credentials.from_service_account_info(credentials, scopes=scope)
    client = gspread.authorize(creds)
    return client

def save_submission_sheets(data):
    """Save submission to Google Sheets"""
    try:
        client = get_google_sheets()
        sheet = client.open_by_key(SPREADSHEET_ID).sheet1
        
        # Check if headers exist, if not add them
        headers = sheet.row_values(1)
        if not headers:
            headers = [
                "Timestamp",
                "Organization",
                "Organization Type",
                "Contact Name",
                "Email",
                "Phone",
                "Partnership Type",
                "Goals",
                "Timeline",
                "Resources",
                "Expectations"
            ]
            sheet.append_row(headers)
        
        # Convert data to row
        row = [
            data["date"],
            data["organization"],
            data["org_type"],
            data["contact_name"],
            data["email"],
            data["phone"],
            data["partnership_type"],
            data["goals"],
            data["timeline"],
            data["resources"],
            data["expectations"]
        ]
        
        sheet.append_row(row)
        return True
    except Exception as e:
        st.error(f"Error saving submission: {str(e)}")
        return False

def get_submissions():
    """Retrieve all submissions from Google Sheets"""
    try:
        client = get_google_sheets()
        sheet = client.open_by_key(SPREADSHEET_ID).sheet1
        data = sheet.get_all_records()
        return data
    except Exception as e:
        st.error(f"Error retrieving submissions: {str(e)}")
        return []