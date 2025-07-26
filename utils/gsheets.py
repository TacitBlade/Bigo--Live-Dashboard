import pandas as pd
import re

def url_to_csv(sheet_url: str) -> str:
    # Convert a Google Sheets URL to a downloadable CSV URL
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
    csv_url = url_to_csv(sheet_url)
    try:
        df: pd.DataFrame = pd.read_csv(csv_url)
    except Exception as e:
        print(f"Error loading sheet: {e}")
        return pd.DataFrame()

    columns_to_keep = ["Date", "Time", "Agency Name.1", "ID1", "Agency Name.2", "ID.2"]
    existing_columns: list[str] = [col for col in columns_to_keep if col in df.columns]
    filtered_df: pd.DataFrame = df.loc[:, existing_columns].dropna(how="all")  # Drop empty rows
    return filtered_df
