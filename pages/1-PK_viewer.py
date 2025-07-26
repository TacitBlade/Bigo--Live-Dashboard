import streamlit as st
import pandas as pd
from utils.gsheet_reader import read_multiple_sheets
from datetime import datetime, timedelta
import time
from io import BytesIO

st.set_page_config(page_title="🏆 PK Viewer", layout="wide")
st.title("🏆 PK Match Viewer")
st.caption("Filter match records, search for hosts, and export to Excel.")

# Sheet URLs
sheet_urls = {
    "Sheet 1": "https://docs.google.com/spreadsheets/d/1T2Za-VeqUe4hN-00X-Qa5T3FAgXMExz2B1Brhspbr7w/edit?gid=920344037",
    "Sheet 2": "https://docs.google.com/spreadsheets/d/1DD7I5sMu55wRVwGjPEv43iygq2b8oudfMspGlOY1zck/edit?gid=1990132269",
    "Sheet 3": "https://docs.google.com/spreadsheets/d/1iS9acwW9DrjZQh_d51_Pv4DcN9_X4alzK3wC2KIWXYw/edit?gid=1234468340",
}

# Auto-refresh
refresh_interval = st.sidebar.selectbox("🔄 Auto-refresh every...", [0, 1, 2, 5, 10], index=2)
if refresh_interval > 0:
    st.caption(f"⏱ Refreshing every {refresh_interval} minute(s).")
    # Use session state to track last refresh time
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    
    current_time = time.time()
    if current_time - st.session_state.last_refresh > refresh_interval * 60:
        st.session_state.last_refresh = current_time
        st.rerun()

@st.cache_data(ttl=300)
def load_data():
    return read_multiple_sheets(sheet_urls)

df = load_data()

# Parse dates
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
today = pd.Timestamp.now().normalize()
this_week = today - timedelta(days=today.weekday())

quick = st.sidebar.radio("📅 Quick Filter", ["All", "Today", "This Week"])
if quick == "Today":
    df = df[df["Date"] == today]
elif quick == "This Week":
    df = df[(df["Date"] >= this_week) & (df["Date"] <= today + timedelta(days=1))]

dates = df["Date"].dt.strftime("%Y-%m-%d").dropna().unique().tolist()
a1s = df["Agency Name.1"].dropna().unique().tolist()
a2s = df["Agency Name.2"].dropna().unique().tolist()

sel_dates = st.sidebar.multiselect("Select Date", sorted(dates), default=dates)
sel_a1 = st.sidebar.multiselect("Agency 1", sorted(a1s), default=a1s)
sel_a2 = st.sidebar.multiselect("Agency 2", sorted(a2s), default=a2s)
search = st.text_input("🔎 Search keyword")

# Apply filters
filtered = df[
    df["Date"].dt.strftime("%Y-%m-%d").isin(sel_dates) &
    df["Agency Name.1"].isin(sel_a1) &
    df["Agency Name.2"].isin(sel_a2)
]
if search:
    s = search.lower()
    filtered = filtered[
        filtered.apply(lambda r: r.astype(str).str.lower().str.contains(s).any(), axis=1)
    ]

st.success(f"✅ {len(filtered)} rows matched 🎯")

# Styled table
def render_table(data: pd.DataFrame) -> str:
    html = "<style>td,th{padding:6px;}table{border-collapse:collapse;width:100%;}th{background:#eee;}</style>"
    html += "<table border='1'><thead><tr>"
    for c in data.columns:
        html += f"<th>{c}</th>"
    html += "</tr></thead><tbody>"
    for i, row in data.iterrows():
        bg = "#ffe5e5" if row["Agency Name.1"] == row["Agency Name.2"] else ("#f9f9f9" if i%2==0 else "#fff")
        html += f"<tr style='background:{bg}'>"
        for val in row:
            html += f"<td>{val}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html

st.markdown(render_table(filtered), unsafe_allow_html=True)

# Excel download
@st.cache_data
def to_excel(df):
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="PK Data")
    return buf.getvalue()

data_xl = to_excel(filtered)
st.download_button(
    "📥 Download Filtered Data (Excel)",
    data=data_xl,
    file_name=f"pk_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
