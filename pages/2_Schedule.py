import streamlit as st
import pandas as pd

st.set_page_config(page_title="📅 PK Schedule", layout="wide")
st.title("📅 Weekly PK Schedule")
st.info("This section will show a host PK timetable or sync with a Google Sheet.")

# Placeholder schedule
schedule_data = {
    "Host": ["prinny_x", "lisalush", "crazybitch"],
    "Monday": ["Talent PK", "Family 2v2", "Mini PK"],
    "Tuesday": ["Rest", "Agency", "Family Team"],
    "Wednesday": ["Talent", "Family", "Agency"],
}
df = pd.DataFrame(schedule_data)
st.table(df)
