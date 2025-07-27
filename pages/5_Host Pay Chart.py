import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# Clean data from the provided pay chart
data = {
    'Ranking': ['V1', 'F', 'F+', 'E', 'E+', 'D', 'D+', 'C', 'C+', 'B', 'B+', 'A', 'A+', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14'],
    'Target Beans': [5000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 130000, 170000, 250000, 350000, 450000, 600000, 800000, 1000000, 1500000, 2000000, 3000000, 4000000, 5000000, 6000000],
    'Salary in Beans': [19110, 18900, 37590, 56280, 74970, 93450, 112350, 131040, 149250, 168000, 185850, 220500, 230700, 236250, 303450, 441000, 617440, 793800, 1024800, 1354500, 1680000, 2478000, 3297000, 4956000, 6426000, 7720000, 8568000],
    'Agency Renumeration': [23, 23, 45, 67, 89, 112, 134, 156, 178, 200, 221, 243, 263, 281, 361, 525, 735, 945, 1220, 1613, 2000, 2950, 3925, 5900, 7650, 9200, 10200],
    'Agency Renumeration Beans': [4830, 4830, 9450, 14070, 18690, 23520, 28140, 32760, 37380, 42000, 46410, 51030, 55230, 59010, 75810, 110250, 154350, 198450, 298200, 380730, 462000, 661500, 866250, 1281000, 1648500, 1974000, 2184000],
    'Agency Renumeration Convert Diamonds': [23, 23, 45, 67, 89, 112, 134, 156, 178, 200, 221, 243, 263, 281, 361, 525, 735, 945, 1220, 1613, 2000, 2950, 3925, 5900, 7650, 9200, 10200]
}

# Create DataFrame
df = pd.DataFrame(data)

# Streamlit app configuration
st.set_page_config(page_title="Host Pay Chart", page_icon="💰", layout="wide")

# App title
st.title("🎯 Official Host Pay Chart")
st.markdown("---")

# Sidebar for filters and options
st.sidebar.header("📊 Chart Options")
chart_type = st.sidebar.selectbox(
    "Select Chart Type",
    ["Data Table", "Target vs Salary", "Ranking Progression", "Agency Remuneration", "All Charts"]
)

# Display metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Rankings", len(df))
with col2:
    st.metric("Highest Target", f"{df['Target Beans'].max():,} beans")
with col3:
    st.metric("Highest Salary", f"{df['Salary in Beans'].max():,} beans")
with col4:
    st.metric("Max Agency Pay", f"{df['Agency Renumeration'].max():,} diamonds")

st.markdown("---")

# Chart display based on selection
if chart_type == "Data Table" or chart_type == "All Charts":
    st.subheader("📋 Complete Pay Chart")
    
    # Format DataFrame for better display
    display_df = df.copy()
    display_df['Target Beans'] = display_df['Target Beans'].apply(lambda x: f"{x:,}")
    display_df['Salary in Beans'] = display_df['Salary in Beans'].apply(lambda x: f"{x:,}")
    display_df['Agency Renumeration Beans'] = display_df['Agency Renumeration Beans'].apply(lambda x: f"{x:,}")
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Ranking": st.column_config.TextColumn("Rank", width="small"),
            "Target Beans": st.column_config.TextColumn("Target", width="medium"),
            "Salary in Beans": st.column_config.TextColumn("Salary", width="medium"),
            "Agency Renumeration": st.column_config.NumberColumn("Agency ($)", width="small"),
            "Agency Renumeration Beans": st.column_config.TextColumn("Agency Beans", width="medium"),
            "Agency Renumeration Convert Diamonds": st.column_config.NumberColumn("Diamonds", width="small")
        }
    )

if chart_type == "Target vs Salary" or chart_type == "All Charts":
    st.subheader("📈 Target Beans vs Salary Comparison")
    
    fig = go.Figure()
    
    # Add target beans
    fig.add_trace(go.Scatter(
        x=df['Ranking'],
        y=df['Target Beans'],
        mode='lines+markers',
        name='Target Beans',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=8)
    ))
    
    # Add salary beans
    fig.add_trace(go.Scatter(
        x=df['Ranking'],
        y=df['Salary in Beans'],
        mode='lines+markers',
        name='Salary in Beans',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Target vs Salary Progression by Ranking",
        xaxis_title="Ranking",
        yaxis_title="Beans",
        hovermode='x unified',
        height=500,
        yaxis=dict(type='log'),  # Log scale for better visualization
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)

if chart_type == "Ranking Progression" or chart_type == "All Charts":
    st.subheader("🎯 Ranking Progression Analysis")
    
    # Calculate salary to target ratio
    df['Salary_to_Target_Ratio'] = df['Salary in Beans'] / df['Target Beans']
    
    fig = px.bar(
        df,
        x='Ranking',
        y='Salary_to_Target_Ratio',
        title="Salary to Target Ratio by Ranking",
        color='Salary_to_Target_Ratio',
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        xaxis_title="Ranking",
        yaxis_title="Salary/Target Ratio",
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)

if chart_type == "Agency Remuneration" or chart_type == "All Charts":
    st.subheader("💎 Agency Remuneration Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.line(
            df,
            x='Ranking',
            y='Agency Renumeration',
            title="Agency Remuneration (Diamonds)",
            markers=True
        )
        fig1.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.area(
            df,
            x='Ranking',
            y='Agency Renumeration Beans',
            title="Agency Remuneration (Beans)",
            color_discrete_sequence=['#FF9F43']
        )
        fig2.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig2, use_container_width=True)

# Interactive calculator
st.markdown("---")
st.subheader("🧮 Pay Calculator")

col1, col2 = st.columns(2)

with col1:
    selected_rank = st.selectbox("Select Ranking:", df['Ranking'].tolist())
    
with col2:
    custom_beans = st.number_input("Or enter custom beans:", min_value=0, value=50000)

# Display calculation results
if selected_rank:
    rank_data = df[df['Ranking'] == selected_rank].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Target:** {rank_data['Target Beans']:,} beans")
    with col2:
        st.success(f"**Salary:** {rank_data['Salary in Beans']:,} beans")
    with col3:
        st.warning(f"**Agency Pay:** {rank_data['Agency Renumeration']} diamonds")

# Export functionality
st.markdown("---")
st.subheader("📥 Export Data")

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Host_Pay_Chart')
        
        # Get workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Host_Pay_Chart']
        
        # Add formatting
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BD',
            'border': 1
        })
        
        # Apply header format
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            
    return output.getvalue()

col1, col2 = st.columns(2)

with col1:
    excel_data = to_excel(df)
    st.download_button(
        label="📊 Export to Excel",
        data=excel_data,
        file_name="Bigo_Live_Host_Pay_Chart.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col2:
    csv_data = df.to_csv(index=False)
    st.download_button(
        label="📋 Export to CSV",
        data=csv_data,
        file_name="Bigo_Live_Host_Pay_Chart.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("*Bigo Live Host Pay Chart Dashboard - Last Updated: July 2025*")