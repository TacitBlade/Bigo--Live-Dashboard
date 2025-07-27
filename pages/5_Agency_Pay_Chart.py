import streamlit as st
import pandas as pd
import io

# Data from the provided Agency Salary sheet
data = {
    'Ranking': ['V1', 'F', 'F+', 'E', 'E+', 'D', 'D+', 'C', 'C+', 'B', 'B+', 'A', 'A+', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14'],
    'Host Target Beans': [5000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 130000, 170000, 250000, 350000, 450000, 600000, 800000, 1000000, 1500000, 2000000, 3000000, 4000000, 5000000, 6000000],
    'S Bonus For Agency': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 200, 200, 200, 200, 200, 200, 200, 200, 200],
    'Total Remuneration (USD)': [23, 23, 45, 67, 89, 112, 134, 156, 178, 200, 221, 243, 263, 281, 361, 525, 735, 945, 1420, 1813, 2200, 3150, 4125, 6100, 7850, 9400, 10400],
    'Beans': [4830, 4830, 9450, 14070, 18690, 23520, 28140, 32760, 37380, 42000, 46410, 51030, 55230, 59010, 75810, 110250, 154350, 198450, 298200, 380730, 462000, 661500, 866250, 1281000, 1648500, 1974000, 2184000],
    'Diamonds': [1324, 1324, 2605, 3888, 5159, 6501, 7782, 9053, 10341, 11620, 12839, 14118, 15287, 16334, 20972, 30518, 42725, 54934, 82550, 105388, 127900, 183124, 239807, 354631, 456361, 546482, 604616]
}

# Create DataFrame
df = pd.DataFrame(data)

# Streamlit app title
st.title("Agency Pay Chart")

# Display the DataFrame with better formatting
st.dataframe(df, use_container_width=True)

# Function to convert DataFrame to Excel
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Agency_Pay_Chart')
        
        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Agency_Pay_Chart']
        
        # Add number formatting for better readability
        number_format = workbook.add_format({'num_format': '#,##0'})
        currency_format = workbook.add_format({'num_format': '$#,##0'})
        
        # Format columns with appropriate number formatting
        worksheet.set_column('B:B', 15, number_format)  # Host Target Beans
        worksheet.set_column('C:C', 15, number_format)  # S Bonus For Agency
        worksheet.set_column('D:D', 20, currency_format)  # Total Remuneration (USD)
        worksheet.set_column('E:E', 15, number_format)  # Beans
        worksheet.set_column('F:F', 15, number_format)  # Diamonds
        
    return output.getvalue()

# Download button for Excel
excel_data = to_excel(df)
st.download_button(
    label="📊 Export to Excel",
    data=excel_data,
    file_name="Agency_Pay_Chart.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)