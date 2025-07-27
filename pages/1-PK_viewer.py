import streamlit as st
import pandas as pd

# === INPUT: Google Sheet ID & GID ===
sheet_id = "1DD7I5sMu55wRVwGjPEv43iygq2b8oudfMspGlOY1zck"  # Replace with your actual sheet ID

# Define available sheets with their GIDs
available_sheets = {
    "Star Task PK": "124426109",
    "Talent PK": "1441823487", 
    "2 vs 2 PK": "1623495727",
    "Agency PK Party": "1135840848",
    "Daily PK": "539805742"
}

# Let user select which sheet to view
selected_sheet = st.sidebar.selectbox("Select PK Type", list(available_sheets.keys()))
gid = available_sheets[selected_sheet]

# === BUILD EXPORT LINK ===
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

# === LOAD DATA FROM SHEET ===
try:
    df = pd.read_csv(csv_url)
except Exception as e:
    st.error(f"Unable to load data: {e}")
    st.stop()

# === CLEAN & SELECT REQUIRED COLUMNS ===
# Fix: Remove duplicate "Agency Name" 
expected_columns = ["Date", "PK Time", "Agency Name", "ID 1", "ID 2"]
missing = [col for col in expected_columns if col not in df.columns]
if missing:
    st.warning(f"Missing expected columns: {missing}")
    st.stop()

df = df[expected_columns]

# === SIDEBAR FILTERS ===
st.sidebar.header("Filters")

# Initialize filtered dataframe
filtered_df = df.copy()

# Date Filter
if "Date" in df.columns:
    date_options = ["All"] + list(df["Date"].dropna().unique())
    selected_date = st.sidebar.selectbox("Filter by Date", date_options)
    if selected_date != "All":
        filtered_df = filtered_df[filtered_df["Date"] == selected_date]

# PK Time Filter
if "PK Time" in df.columns:
    pk_time_options = ["All"] + list(df["PK Time"].dropna().unique())
    selected_pk_time = st.sidebar.selectbox("Filter by PK Time", pk_time_options)
    if selected_pk_time != "All":
        filtered_df = filtered_df[filtered_df["PK Time"] == selected_pk_time]

# Agency Name Filter
if "Agency Name" in df.columns:
    agency_options = ["All"] + sorted(list(df["Agency Name"].dropna().unique()))
    selected_agency = st.sidebar.selectbox("Filter by Agency Name", agency_options)
    if selected_agency != "All":
        filtered_df = filtered_df[filtered_df["Agency Name"] == selected_agency]

# ID 1 Filter
if "ID 1" in df.columns:
    id1_options = ["All"] + list(df["ID 1"].dropna().unique())
    selected_id1 = st.sidebar.selectbox("Filter by ID 1", id1_options)
    if selected_id1 != "All":
        filtered_df = filtered_df[filtered_df["ID 1"] == selected_id1]

# ID 2 Filter
if "ID 2" in df.columns:
    id2_options = ["All"] + list(df["ID 2"].dropna().unique())
    selected_id2 = st.sidebar.selectbox("Filter by ID 2", id2_options)
    if selected_id2 != "All":
        filtered_df = filtered_df[filtered_df["ID 2"] == selected_id2]

# === DISPLAY ===
st.title("UK Agency & Host Events")

# Show filter summary
active_filters = []
if 'selected_date' in locals() and selected_date != "All":
    active_filters.append(f"Date: {selected_date}")
if 'selected_pk_time' in locals() and selected_pk_time != "All":
    active_filters.append(f"PK Time: {selected_pk_time}")
if 'selected_agency' in locals() and selected_agency != "All":
    active_filters.append(f"Agency: {selected_agency}")
if 'selected_id1' in locals() and selected_id1 != "All":
    active_filters.append(f"ID 1: {selected_id1}")
if 'selected_id2' in locals() and selected_id2 != "All":
    active_filters.append(f"ID 2: {selected_id2}")

if active_filters:
    st.markdown(f"**Active Filters:** {', '.join(active_filters)}")
else:
    st.markdown("**Showing all data**")

st.markdown(f"**Total records:** {len(filtered_df)}")
st.dataframe(filtered_df)