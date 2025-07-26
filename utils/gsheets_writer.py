import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def get_client():
    """Get authenticated Google Sheets client with error handling"""
    credentials_file = "google_credentials.json"
    
    if not os.path.exists(credentials_file):
        raise FileNotFoundError(f"Google credentials file '{credentials_file}' not found. Please ensure it exists in the project root.")
    
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, SCOPES)
        return gspread.authorize(credentials)
    except Exception as e:
        raise Exception(f"Failed to authenticate with Google Sheets: {str(e)}")

def extract_sheet_id(url: str) -> str:
    """Extract sheet ID from Google Sheets URL"""
    parts = url.split("/d/")
    if len(parts) < 2:
        raise ValueError("Invalid Google Sheets URL format")
    return parts[1].split("/")[0]

def write_dataframe_to_sheet(sheet_url: str, worksheet_name: str, df: pd.DataFrame, clear_existing=True):
    """Write DataFrame to Google Sheets with comprehensive error handling"""
    try:
        gc = get_client()
        sheet_id = extract_sheet_id(sheet_url)
        sh = gc.open_by_key(sheet_id)

        try:
            ws = sh.worksheet(worksheet_name)
        except gspread.exceptions.WorksheetNotFound:
            ws = sh.add_worksheet(title=worksheet_name, rows="1000", cols="26")

        if clear_existing:
            ws.clear()

        # Convert DataFrame to values, handling NaN values
        df_clean = df.fillna('')  # Replace NaN with empty strings
        data = [df_clean.columns.values.tolist()] + df_clean.values.tolist()
        
        # Update worksheet
        ws.update(data)
        
        return True
        
    except FileNotFoundError as e:
        raise Exception(f"Credentials error: {str(e)}")
    except gspread.exceptions.APIError as e:
        raise Exception(f"Google Sheets API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to write to Google Sheet: {str(e)}")
