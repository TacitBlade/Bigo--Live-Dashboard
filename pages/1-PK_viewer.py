import streamlit as st

st.set_page_config(page_title="Bigo Dashboard", layout="wide")
st.title("🎥 Welcome to the Bigo Agency Dashboard")

st.markdown("Select a page from the sidebar to begin 👉")
st.info("Use the sidebar navigation to switch between **PK Viewer**, **Schedule**, and **Pay**.")
st.success(f"✅ {len(filtered_df)} rows matched your filters 🎯")
