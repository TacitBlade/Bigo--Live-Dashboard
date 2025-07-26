import pandas as pd
import re
from typing import Optional
import requests

def url_to_csv(sheet_url: str) -> str:
    """Convert a Google Sheets URL to a downloadable CSV URL"""
    base_url = sheet_url.split('/edit')[0]
    
    # Extract gid from URL - handle both fragment (#gid=) and query parameter (?gid=) formats
    gid = "0"  # Default gid
    if "gid=" in sheet_url:
        # Handle fragment format: #gid=123
        if "#gid=" in sheet_url:
            gid = sheet_url.split("#gid=")[-1].split("&")[0]
        # Handle query parameter format: ?gid=123
        elif "?gid=" in sheet_url or "&gid=" in sheet_url:
            gid_match = re.search(r'[?&]gid=([^&]+)', sheet_url)
            if gid_match:
                gid = gid_match.group(1)
    
    return f"{base_url}/export?format=csv&gid={gid}"

def read_filtered_columns(sheet_url: str) -> pd.DataFrame:
    """Read specific columns from a Google Sheet and return filtered DataFrame"""
    csv_url = url_to_csv(sheet_url)
    
    try:
        # First check if the URL is accessible
        response = requests.head(csv_url, timeout=10)
        if response.status_code != 200:
            print(f"Warning: Sheet URL returned status {response.status_code}")
            return pd.DataFrame()
        
        # Read the CSV data
        df = pd.read_csv(csv_url)
        
        # Define columns to extract
        columns_to_keep = ["Date", "Time", "Agency Name.1", "ID1", "Agency Name.2", "ID.2"]
        existing_columns = [col for col in columns_to_keep if col in df.columns]
        
        if not existing_columns:
            print(f"Warning: None of the expected columns found in sheet")
            return pd.DataFrame()
        
        # Filter and clean the data
        filtered_df = df.loc[:, existing_columns].dropna(how="all")  # Drop empty rows
        
    except requests.exceptions.RequestException as e:
        print(f"Network error loading sheet: {str(e)}")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        print("Warning: Sheet appears to be empty")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error loading sheet: {str(e)}")
        return pd.DataFrame()
    
    return filtered_df
