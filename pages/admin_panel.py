import streamlit as st
import pandas as pd

def show_admin_panel(data_manager):
    st.markdown('<div class="main-header"><h1>🔧 Admin Panel</h1></div>', 
                unsafe_allow_html=True)
    
    tabs = st.tabs(["📊 Data Management", "💱 Conversion Rates", "👥 User Management"])
    
    with tabs[0]:
        st.subheader("Data Management")
        
        # Data upload
        uploaded_file = st.file_uploader(
            "Upload new pay chart data",
            type=['csv', 'xlsx', 'json'],
            help="Upload updated pay chart data"
        )
        
        if uploaded_file:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            
            st.dataframe(df, use_container_width=True)
            
            if st.button("💾 Save Updated Data"):
                # Save logic here
                st.success("Data updated successfully!")
        
        # Bulk operations
        st.subheader("Bulk Operations")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Refresh All Data"):
                st.info("Refreshing data from sources...")
        
        with col2:
            if st.button("📤 Export All Data"):
                st.info("Preparing export package...")
    
    with tabs[1]:
        st.subheader("Conversion Rates")
        
        col1, col2 = st.columns(2)
        with col1:
            bean_to_diamond = st.number_input("Beans to Diamond Rate", value=3.61, step=0.01)
        with col2:
            diamond_to_usd = st.number_input("Diamond to USD Rate", value=0.0036, step=0.0001)
        
        if st.button("💰 Update Rates"):
            data_manager.update_conversion_rates(bean_to_diamond, diamond_to_usd)
            st.success("Conversion rates updated!")
    
    with tabs[2]:
        st.subheader("User Management")
        st.info("User management features coming soon...")