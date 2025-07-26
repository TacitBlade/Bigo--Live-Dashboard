import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def get_client():
    credentials = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", SCOPES)
    return gspread.authorize(credentials)

def extract_sheet_id(url: str) -> str:
    parts = url.split("/d/")
    if len(parts) < 2:
        raise ValueError("Invalid Google Sheets URL")
    return parts[1].split("/")[0]

def write_dataframe_to_sheet(sheet_url: str, worksheet_name: str, df: pd.DataFrame, clear_existing=True):
    gc = get_client()
    sheet_id = extract_sheet_id(sheet_url)
    sh = gc.open_by_key(sheet_id)

    try:
        ws = sh.worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=worksheet_name, rows="1000", cols="26")

    if clear_existing:
        ws.clear()

    # Include headers
    ws.update([df.columns.values.tolist()] + df.values.tolist())
