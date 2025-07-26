import streamlit as st
import pandas as pd

# === INPUT: Google Sheet ID & GID ===
sheet_id = "1DD7I5sMu55wRVwGjPEv43iygq2b8oudfMspGlOY1zck"  # Replace with your actual sheet ID
gid = "1135840848"            # Replace with the correct tab's GID (not the Sign Up Rewards tab)

# === BUILD EXPORT LINK ===
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

# === LOAD DATA FROM SHEET ===
try:
    df = pd.read_csv(csv_url)
except Exception as e:
    st.error(f"Unable to load data: {e}")
    st.stop()

# === CLEAN & SELECT REQUIRED COLUMNS ===
expected_columns = ["Date", "PK Time", "Agency Name ID 1", "Agency Name UID 2"]
missing = [col for col in expected_columns if col not in df.columns]
if missing:
    st.warning(f"Missing expected columns: {missing}")
    st.stop()

df = df[expected_columns]

# === SIDEBAR FILTER ===
agency_options = df["Agency Name ID 1"].dropna().unique()
selected_agency = st.sidebar.selectbox("Filter by Agency Name", agency_options)

# === FILTER DATA ===
filtered_df = df[df["Agency Name ID 1"] == selected_agency]

# === DISPLAY ===
st.title("UK Agency & Host Events")
st.markdown(f"Showing results for **{selected_agency}**")
st.dataframe(filtered_df)