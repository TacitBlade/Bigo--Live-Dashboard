# Cache configuration for better performance
import streamlit as st

# Cache settings
CACHE_TTL = 300  # 5 minutes
MAX_ENTRIES = 100

def configure_cache():
    """Configure Streamlit cache settings"""
    # Clear cache if needed
    if st.button("🔄 Clear Cache", help="Clear all cached data to force refresh"):
        st.cache_data.clear()
        st.success("Cache cleared! Data will be refreshed on next load.")
