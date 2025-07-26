import streamlit as st
import pandas as pd
from utils.gsheet_reader import read_filtered_columns

st.set_page_config(page_title="Bigo Matchup Viewer", layout="wide")

st.title("📊 Bigo PK Match Data Viewer")

# Load data from all 3 sheets
sheet_urls = {
    "Sheet 1": "https://docs.google.com/spreadsheets/d/1T2Za-VeqUe4hN-00X-Qa5T3FAgXMExz2B1Brhspbr7w/edit?gid=920344037",
    "Sheet 2": "https://docs.google.com/spreadsheets/d/1DD7I5sMu55wRVwGjPEv43iygq2b8oudfMspGlOY1zck/edit?gid=1990132269",
    "Sheet 3": "https://docs.google.com/spreadsheets/d/1iS9acwW9DrjZQh_d51_Pv4DcN9_X4alzK3wC2KIWXYw/edit?gid=1234468340",
}

all_dfs = []
for name, url in sheet_urls.items():
    df = read_filtered_columns(url)
    df["Source Sheet"] = name
    all_dfs.append(df)

combined_df = pd.concat(all_dfs, ignore_index=True)

# Sidebar filters
st.sidebar.header("🔍 Filter Data")

date_options = sorted(combined_df["Date"].dropna().unique())
agency1_options = sorted(combined_df["Agency Name.1"].dropna().unique())
agency2_options = sorted(combined_df["Agency Name.2"].dropna().unique())

selected_date = st.sidebar.multiselect("Select Date", date_options, default=date_options)
selected_agency1 = st.sidebar.multiselect("Agency Name 1", agency1_options, default=agency1_options)
selected_agency2 = st.sidebar.multiselect("Agency Name 2", agency2_options, default=agency2_options)

# Apply filters
filtered_df = combined_df[
    combined_df["Date"].isin(selected_date) &
    combined_df["Agency Name.1"].isin(selected_agency1) &
    combined_df["Agency Name.2"].isin(selected_agency2)
]

st.success(f"{len(filtered_df)} rows matched your filters.")

# Display table
st.dataframe(filtered_df, use_container_width=True)

# Excel download
@st.cache_data
def convert_to_excel(df):
    import io
    from openpyxl import Workbook
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
