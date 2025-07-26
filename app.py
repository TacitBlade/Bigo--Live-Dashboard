import streamlit as st
import pandas as pd
from utils.gsheets import read_filtered_columns
from datetime import timedelta
import time

# Load custom CSS
def load_css():
    try:
        with open('static/style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # CSS file is optional

# ---- Config ----
st.set_page_config(page_title="Bigo PK Dashboard", layout="wide")
load_css()  # Load custom styles

st.title("📊 Bigo PK Match Data Viewer")

st.markdown("Select a page from the sidebar to begin 👉")
st.info("Use the sidebar navigation to switch between **PK Viewer**, **Schedule**, and **Pay**.")

# --- Auto Refresh ---
refresh_interval = st.sidebar.selectbox("🔄 Auto-refresh every...", [0, 1, 2, 5, 10], index=0)
if refresh_interval > 0:
    st.caption(f"⏱ Auto-refreshing every {refresh_interval} minute(s).")
    # Use session state to track last refresh time
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    
    current_time = time.time()
    if current_time - st.session_state.last_refresh > refresh_interval * 60:
        st.session_state.last_refresh = current_time
        st.rerun()

# --- Load sheets ---
sheet_urls = {
    "Sheet 1": "https://docs.google.com/spreadsheets/d/1T2Za-VeqUe4hN-00X-Qa5T3FAgXMExz2B1Brhspbr7w/edit?gid=920344037",
    "Sheet 2": "https://docs.google.com/spreadsheets/d/1DD7I5sMu55wRVwGjPEv43iygq2b8oudfMspGlOY1zck/edit?gid=1990132269",
    "Sheet 3": "https://docs.google.com/spreadsheets/d/1iS9acwW9DrjZQh_d51_Pv4DcN9_X4alzK3wC2KIWXYw/edit?gid=1234468340",
}
sheet_map = {
    "Training PKs": "https://docs.google.com/spreadsheets/d/1T2Za-VeqUe4hN-00X-Qa5T3FAgXMExz2B1Brhspbr7w/edit?gid=920344037",
    "Tasks": "https://docs.google.com/spreadsheets/d/1DD7I5sMu55wRVwGjPEv43iygq2b8oudfMspGlOY1zck/edit?gid=1990132269",
    "Mystery Matches": "https://docs.google.com/spreadsheets/d/1iS9acwW9DrjZQh_d51_Pv4DcN9_X4alzK3wC2KIWXYw/edit?gid=1234468340",
}

selected_sheet_name = st.sidebar.selectbox("📋 Select PK Sheet", options=sheet_map.keys())
selected_sheet_url = sheet_map[selected_sheet_name]

if st.button("✍️ Save back to Google Sheet"):
    write_dataframe_to_sheet(
        sheet_url=sheet_map[selected_sheet_name],
        worksheet_name="StreamlitExport",
        df=filtered_df
    )
    st.success("Sheet updated successfully ✅")


df = read_filtered_columns(selected_sheet_url)

@st.cache_data(ttl=300)
def load_all_data() -> pd.DataFrame:
    all_dfs = []
    for name, url in sheet_urls.items():
        df = read_filtered_columns(url)
        df["Source Sheet"] = name
        all_dfs.append(df)
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    else:
        return pd.DataFrame()

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
else:
    st.sidebar.info("📋 No data available for date filtering")

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

st.success(f"✅ {len(filtered_df)} rows matched your filters.")

# Display data if available
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
else:
    st.warning("⚠️ No data available or no matches found with current filters.")

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
