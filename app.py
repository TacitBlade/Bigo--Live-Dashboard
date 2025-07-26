import streamlit as st

st.set_page_config(page_title="Bigo Dashboard", layout="wide")
st.title("🎥 Welcome to the Bigo Agency Dashboard")

st.markdown("Select a page from the sidebar to begin 👉")
st.info("Use the sidebar navigation to switch between **PK Viewer**, **Schedule**, and **Pay**.")

st.markdown("""
## 📋 Available Pages:
- **🏆 PK Viewer**: View and filter PK match data from Google Sheets
- **📅 Schedule**: View weekly PK schedules for hosts
- **💸 Pay**: Automated paysheet calculations for hosts

## 🔧 Features:
- Real-time data from Google Sheets
- Interactive filtering and search
- Export to Excel functionality
- Responsive design
""")

# --- Footer ---
st.markdown("---")
st.caption("🚀 Bigo Live Dashboard v1.0 | Built with Streamlit")