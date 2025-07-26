import streamlit as st
import pandas as pd
from utils.gsheets import read_filtered_columns
from utils.gsheets_writer import write_dataframe_to_sheet
from utils.data_validator import safe_date_conversion, clean_text_data, display_data_info
from datetime import timedelta
import time

# Load custom CSS
def load_css():
    css_files = ['static/enhanced_style.css', 'static/style.css']
    for css_file in css_files:
        try:
            with open(css_file) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
                break  # Use the first available CSS file
        except FileNotFoundError:
            continue

# ---- Config ----
st.set_page_config(page_title="Bigo PK Dashboard", layout="wide")
load_css()  # Load custom styles

st.title("📊 Bigo PK Match Data Viewer")

st.markdown("Select a page from the sidebar to begin 👉")
st.info("Use the sidebar navigation to switch between **PK Viewer**, **Schedule**, and **Pay**.")

# --- Auto Refresh and Cache Management ---
col1, col2 = st.sidebar.columns(2)

with col1:
    refresh_interval = st.selectbox("🔄 Auto-refresh every...", [0, 1, 2, 5, 10], index=0)

with col2:
    if st.button("🗑️ Clear Cache"):
        st.cache_data.clear()
        st.success("Cache cleared!")
        st.rerun()

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

@st.cache_data(ttl=300)
def load_all_data() -> pd.DataFrame:
    all_dfs = []
    for name, url in sheet_urls.items():
        try:
            df = read_filtered_columns(url)
            if not df.empty:
                df["Source Sheet"] = name
                all_dfs.append(df)
        except Exception as e:
            st.warning(f"⚠️ Could not load {name}: {str(e)}")
    
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    else:
        return pd.DataFrame()

# Load the combined data
combined_df = load_all_data()

# Clean and validate the data
if not combined_df.empty:
    combined_df = clean_text_data(combined_df)
    combined_df = safe_date_conversion(combined_df)

# Display data info
if not combined_df.empty:
    display_data_info(combined_df, "Combined Data Summary")

# --- Sidebar filters ---
st.sidebar.header("🔍 Filter Data")

# Quick date filters
if not combined_df.empty and "Date" in combined_df.columns:
    today = pd.Timestamp.now().normalize()
    this_week = today - timedelta(days=today.weekday())

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

# Save to Google Sheet button (now filtered_df is defined)
if st.button("✍️ Save back to Google Sheet"):
    if not filtered_df.empty:
        try:
            write_dataframe_to_sheet(
                sheet_url=sheet_map[selected_sheet_name],
                worksheet_name="StreamlitExport",
                df=filtered_df
            )
            st.success("Sheet updated successfully ✅")
        except Exception as e:
            st.error(f"Error saving to sheet: {str(e)}")
    else:
        st.warning("No data to save!")

st.success(f"✅ {len(filtered_df)} rows matched your filters.")

# Display data if available
if not filtered_df.empty:
    # --- Styled Table with Conditional Highlight ---
    def render_html_table(df: pd.DataFrame) -> str:
        html = "<style>td, th {padding: 6px 12px;} table {border-collapse: collapse; width: 100%; font-size: 15px;} th {background: #eee;}</style>"
        html += "<table border='1'>"
        html += "<thead><tr>" + "".join([f"<th>{col}</th>" for col in df.columns]) + "</tr></thead><tbody>"

        for idx, (_, row) in enumerate(df.iterrows()):
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
    try:
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="PK Data")
        return output.getvalue()
    except Exception as e:
        st.error(f"Error creating Excel file: {str(e)}")
        return b""

if not filtered_df.empty:
    excel_data = convert_to_excel(filtered_df)
    if excel_data:
        st.download_button(
            label="📥 Download Filtered Data (Excel)",
            data=excel_data,
            file_name="bigo_pk_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
