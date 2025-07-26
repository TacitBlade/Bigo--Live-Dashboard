st.set_page_config(page_title="🏆 PK Viewer", layout="wide")
st.title("🏆 PK Match Viewer")
st.caption("Filter match records, search for hosts, and export to Excel.")
st.success(f"✅ {len(filtered_df)} rows matched your filters 🎯")
