import pandas as pd

def url_to_csv(sheet_url: str) -> str:
    base_url = sheet_url.split('/edit')[0]
    gid = sheet_url.split("gid=")[-1]
    return f"{base_url}/export?format=csv&gid={gid}"

def read_filtered_columns(sheet_url: str) -> pd.DataFrame:
    csv_url = url_to_csv(sheet_url)
    try:
        df = pd.read_csv(csv_url)
    except Exception as e:
        st.error(f"Error loading sheet: {e}")
        return pd.DataFrame()
    cols = ["Date", "Time", "Agency Name.1", "ID1", "Agency Name.2", "ID.2"]
    existing = [c for c in cols if c in df.columns]
    return df[existing].dropna(how="all")

def read_multiple_sheets(sheet_dict: dict) -> pd.DataFrame:
    all_dfs = []
    for name, url in sheet_dict.items():
        df = read_filtered_columns(url)
        df["Source Sheet"] = name
        all_dfs.append(df)
    return pd.concat(all_dfs, ignore_index=True)
