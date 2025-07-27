import streamlit as st
import pandas as pd
import io

# Sample data from the provided pay chart
data = {
    'Ranking': ['V1', 'F', 'F+', 'E', 'E+', 'D', 'D+', 'C', 'C+', 'B', 'B+', 'A', 'A+', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14'],
    'Target Beans': [5000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 130000, 170000, 250000, 350000, 450000, 600000, 800000, 1000000, 1500000, 2000000, 3000000, 4000000, 5000000, 6000000],
    'Salary in Beans': [19110, 18900, 37590, 56280, 74970, 93450, 112350, 131040, 149250, 168000, 185850, 220500, 230700, Ranking,Target Beans,Salary in Beans,Agency Renumeration,Agency Renumeration Beans,Agency Renumeration Convert Diamonds
V1,5000,19110,23,4830,23
F,10000,18900,23,4830,23
F+,20000,37590,45,9450,45
E,30000,56280,67,14070,67
E+,40000,74970,89,18690,89
D,50000,93450,112,23520,112
D+,60000,112350,134,28140,134
C,70000,131040,156,32760,156
C+,80000,149250,178,37380,178
B,90000,168000,200,42000,200
B+,100000,185850,221,46410,221
A,110000,220500,243,51030,243
A+,120000,230700,263,55230,263
S1,130000,236250,281,59010,281
S2,170000,303450,361,75810,361
S3,250000,441000,525,110250,525
S4,350000,617440,735,154350,735
S5,450000,793800,945,198450,945
S6,600000,1024800,1220,298200,1220
S7,800000,1354500,1613,380730,1613
S8,1000000,1680000,2000,462000,2000
S9,1500000,2478000,2950,661500,2950
S10,2000000,3297000,3925,866250,3925
S11,3000000,4956000,5900,1281000,5900
S12,4000000,6426000,7650,1648500,7650
S13,5000000,7720000,9200,1974000,9200
S14,6000000,8568000,10200,2184000,10200
236250, 303450, 441000, 617440, 793800, 1024800, 1354500, 1680000, 2478000, 3297000, 4956000, 6426000, 7720000, 8568000],
    'Agency Renumeration': [23, 23, 45, 67, 89, 112, 134, 156, 178, 200, 221, 243, 263, 281, 361, 525, 735, 945, 1220, 1613, 2000, 2950, 3925, 5900, 7650, 9200, 10200],
    'Agency Renumeration Beans': [4830, 4830, 9450, 14070, 18690, 23520, 28140, 32760, 37380, 42000, 46410, 51030, 55230, 59010, 75810, 110250, 154350, 198450, 298200, 380730, 462000, 661500, 866250, 1281000, 1648500, 1974000, 2184000],
    'Agency Renumeration Convert Diamonds': [23, 23, 45, 67, 89, 112, 134, 156, 178, 200, 221, 243, 263, 281, 361, 525, 735, 945, 1220, 1613, 2000, 2950, 3925, 5900, 7650, 9200, 10200]
}

# Create DataFrame
df = pd.DataFrame(data)

# Streamlit app title
st.title("Officail Host Pay Chart")

# Display the DataFrame
st.dataframe(df, use_container_width=True)

# Function to convert DataFrame to Excel
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

# Download button for Excel
excel_data = to_excel(df)
st.download_button(
    label="Export to Excel",
    data=excel_data,
    file_name="Alpha_Omega_Agency_Pay_Chart.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)