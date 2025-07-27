import streamlit as st
import pandas as pd
import io

# Updated data from the provided Host Pay Chart
data = {
    'Ranking': ['V1', 'F', 'F+', 'E', 'E+', 'D', 'D+', 'C', 'C+', 'B', 'B+', 'A', 'A+', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14'],
    'Target Beans': [5000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 130000, 170000, 250000, 350000, 450000, 600000, 800000, 1000000, 1500000, 2000000, 3000000, 4000000, 5000000, 6000000],
    'Salary in Beans': [19110, 18900, 37590, 56280, 74970, 93450, 112350, 131040, 149250, 168000, 185850, 220500, 230700, 236250, 303450, 441000, 617440, 793800, 1024800, 1354500, 1680000, 2478000, 3297000, 4956000, 6426000, 7720000, 8568000],
    'Salary in Diamonds': [5497, 5215, 10397, 15574, 20738, 25862, 31095, 36267, 41310, 46504, 51434, 61036, 63850, 65395, 83996, 122085, 170925, 219747, 283696, 374973, 465089, 686010, 912743, 1372025, 1778985, 2137216, 2371977]
}

# Create DataFrame
df = pd.DataFrame(data)

# Streamlit app title
st.title("Host Pay Chart")

# Display the DataFrame with better formatting
st.dataframe(df, use_container_width=True)

# Function to convert DataFrame to Excel
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Host_Pay_Chart')
        
        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Host_Pay_Chart']
        
        # Add number formatting for better readability
        number_format = workbook.add_format({'num_format': '#,##0'})
        worksheet.set_column('B:D', 15, number_format)
        
    return output.getvalue()

# Download button for Excel
excel_data = to_excel(df)
st.download_button(
    label="📊 Export to Excel",
    data=excel_data,
    file_name="Host_Pay_Chart.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)