import streamlit as st
import pandas as pd
from utils.gsheets import read_filtered_columns
from datetime import timedelta
import time

st.set_page_config(page_title="📊 PK Viewer", layout="wide")
st.title("📊 PK Match Data Viewer")

st.info("🔍 Use the filters below to explore PK match data across multiple sheets.")

# --- Load sheets ---
sheet_urls = {
    "Sheet 1": "https://docs.google.com/spreadsheets/d/1T2Za-VeqUe4hN-00X-Qa5T3FAgXMExz2B1Brhspbr7w/edit?gid=920344037",
    "Sheet 2": "https://docs.google.com/spreadsheets/d/1DD7I5sMu55wRVwGjPEv43iygq2b8oudfMspGlOY1zck/edit?gid=1990132269",
    "Sheet 3": "https://docs.google.com/spreadsheets/d/1iS9acwW9DrjZQh_d51_Pv4DcN9_X4alzK3wC2KIWXYw/edit?gid=1234468340",
}

@st.cache_data(ttl=300)
def load_all_data() -> pd.DataFrame:
    all_dfs = []
    for name, url in sheet_urls.items():
        try:
            df = read_filtered_columns(url)
            df["Source Sheet"] = name
            all_dfs.append(df)
        except Exception as e:
            st.warning(f"⚠️ Could not load {name}: {str(e)}")
    
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    else:
        return pd.DataFrame()

# Load data
with st.spinner("📊 Loading PK data..."):
    combined_df = load_all_data()

# Ensure date is in datetime format
if not combined_df.empty and "Date" in combined_df.columns:
    try:
        combined_df["Date"] = pd.to_datetime(combined_df["Date"], errors='coerce')
    except Exception as e:
        st.warning(f"⚠️ Date conversion error: {str(e)}")

# --- Sidebar filters ---
st.sidebar.header("🔍 Filter Data")

# Quick date filters
if not combined_df.empty and "Date" in combined_df.columns:
    today = pd.Timestamp.now().normalize()
    this_week = today - pd.to_timedelta(today.weekday(), unit='D')

    quick_filter = st.sidebar.radio("📅 Quick Filter", ["All", "Today", "This Week"])

    if quick_filter == "Today":
        combined_df = combined_df[combined_df["Date"].dt.date == today.date()]
    elif quick_filter == "This Week":
        combined_df = combined_df[(combined_df["Date"] >= this_week) & (combined_df["Date"] <= today + timedelta(days=1))]

# Regular filters
if not combined_df.empty:
    if "Date" in combined_df.columns:
        date_options = sorted(combined_df["Date"].dropna().dt.strftime("%Y-%m-%d").unique())
    else:
        date_options = []
    
    if "Agency Name.1" in combined_df.columns:
        agency1_options = sorted(combined_df["Agency Name.1"].dropna().unique())
    else:
        agency1_options = []
    
    if "Agency Name.2" in combined_df.columns:
        agency2_options = sorted(combined_df["Agency Name.2"].dropna().unique())
    else:
        agency2_options = []
else:
    date_options = []
    agency1_options = []
    agency2_options = []

selected_date = st.sidebar.multiselect("Select Date", date_options, default=date_options)
selected_agency1 = st.sidebar.multiselect("Agency Name 1", agency1_options, default=agency1_options)
selected_agency2 = st.sidebar.multiselect("Agency Name 2", agency2_options, default=agency2_options)

# Search box
search_text = st.text_input("🔎 Search any keyword (ID, Agency, Date, etc.)")

# Apply filters
if not combined_df.empty:
    filtered_df = combined_df.copy()
    
    # Apply date filter
    if selected_date and "Date" in combined_df.columns:
        filtered_df = filtered_df[filtered_df["Date"].dt.strftime("%Y-%m-%d").isin(selected_date)]
    
    # Apply agency filters
    if selected_agency1 and "Agency Name.1" in combined_df.columns:
        filtered_df = filtered_df[filtered_df["Agency Name.1"].isin(selected_agency1)]
    
    if selected_agency2 and "Agency Name.2" in combined_df.columns:
        filtered_df = filtered_df[filtered_df["Agency Name.2"].isin(selected_agency2)]
else:
    filtered_df = combined_df.copy()

# Apply search
if search_text and not filtered_df.empty:
    search_text = search_text.lower()
    mask = filtered_df.astype(str).apply(lambda x: x.str.lower().str.contains(search_text, na=False)).any(axis=1)
    filtered_df = filtered_df[mask]

st.success(f"✅ {len(filtered_df)} rows matched your filters 🎯")

# --- Display data ---
if not filtered_df.empty:
    # --- Styled Table with Conditional Highlight ---
    def render_html_table(df: pd.DataFrame) -> str:
        html = "<style>td, th {padding: 6px 12px;} table {border-collapse: collapse; width: 100%; font-size: 15px;} th {background: #eee;}</style>"
        html += "<table border='1'>"
        html += "<thead><tr>" + "".join([f"<th>{col}</th>" for col in df.columns]) + "</tr></thead><tbody>"

        for idx, (i, row) in enumerate(df.iterrows()):
            # Highlight if agencies are the same
            bg_color = "#ffe5e5" if row.get("Agency Name.1") == row.get("Agency Name.2") else ("#f9f9f9" if idx % 2 == 0 else "#ffffff")
            html += f"<tr style='background-color:{bg_color}'>" + "".join(
                [f"<td>{str(cell)}</td>" for cell in row]) + "</tr>"
        html += "</tbody></table>"
        return html

    st.markdown(render_html_table(filtered_df), unsafe_allow_html=True)

    # --- Download to Excel ---
    @st.cache_data
    def convert_to_excel(df: pd.DataFrame) -> bytes:
        import io
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="PK Data")
        return output.getvalue()

    excel_data = convert_to_excel(filtered_df)
    st.download_button(
        label="📥 Download Filtered Data (Excel)",
        data=excel_data,
        file_name="bigo_pk_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.warning("⚠️ No data available. Please check your Google Sheets URLs and internet connection.")
