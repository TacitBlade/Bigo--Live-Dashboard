import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show_analytics(data_manager, user_role):
    st.markdown('<div class="main-header"><h1>📊 Analytics Dashboard</h1></div>', 
                unsafe_allow_html=True)
    
    # Load data
    host_data = data_manager.load_data('host_pay')
    agency_data = data_manager.load_data('agency_pay')
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Rankings", len(host_data), "27 levels")
    with col2:
        st.metric("Max Host Salary", f"${host_data['Salary in Diamonds'].max():,.0f}", "S14 Level")
    with col3:
        st.metric("Max Agency Pay", f"${agency_data['Total Remuneration (USD)'].max():,.0f}", "S14 Level")
    with col4:
        st.metric("Top Target Beans", f"{host_data['Target Beans'].max():,}", "6M beans")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Host Pay Progression
        fig1 = px.line(host_data, x='Ranking', y='Salary in Diamonds', 
                      title='Host Salary Progression',
                      markers=True)
        fig1.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Agency vs Host Comparison
        comparison_data = host_data.merge(agency_data, on='Ranking', suffixes=('_host', '_agency'))
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=comparison_data['Ranking'], 
                                 y=comparison_data['Salary in Diamonds'], 
                                 name='Host Salary', mode='lines+markers'))
        fig2.add_trace(go.Scatter(x=comparison_data['Ranking'], 
                                 y=comparison_data['Total Remuneration (USD)'], 
                                 name='Agency Pay', mode='lines+markers'))
        fig2.update_layout(title='Host vs Agency Pay Comparison',
                          xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Interactive filters
    st.subheader("🔍 Interactive Analysis")
    
    ranking_filter = st.multiselect(
        "Select Rankings to Analyze",
        options=host_data['Ranking'].tolist(),
        default=host_data['Ranking'].tolist()[-5:]  # Last 5 rankings
    )
    
    if ranking_filter:
        filtered_data = host_data[host_data['Ranking'].isin(ranking_filter)]
        
        # Detailed table
        st.dataframe(filtered_data, use_container_width=True)
        
        # Export filtered data
        csv = filtered_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data",
            data=csv,
            file_name=f"filtered_analysis_{len(ranking_filter)}_rankings.csv",
            mime="text/csv"
        )