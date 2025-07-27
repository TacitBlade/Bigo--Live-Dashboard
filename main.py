import streamlit as st
from utils.navigation import NavigationManager
from utils.data_manager import DataManager
from pages import *

# Configure page
st.set_page_config(
    page_title="Bigo Live Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize managers
nav_manager = NavigationManager()
data_manager = DataManager()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Navigation
    selected_page, user_role = nav_manager.render_sidebar()
    
    # Route to pages
    if selected_page == "main_dashboard":
        show_main_dashboard(data_manager, user_role)
    elif selected_page == "host_pay_chart":
        show_host_pay_chart(data_manager)
    elif selected_page == "agency_pay_chart":
        show_agency_pay_chart(data_manager)
    elif selected_page == "analytics":
        show_analytics(data_manager, user_role)
    elif selected_page == "admin_panel":
        show_admin_panel(data_manager)
    elif selected_page == "reports":
        show_reports(data_manager, user_role)
    elif selected_page == "settings":
        show_settings(data_manager)

if __name__ == "__main__":
    main()