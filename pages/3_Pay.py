import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="💸 Pay Sheet", layout="wide")
st.title("💸 Host Pay Calculator")

st.markdown("Use this tool to calculate host salary beans and bonuses under the Streamer Plan Policy effective March 1, 2025.")

st.markdown(
    "- Enter each host's **Local Beans** and **Overseas Beans** earned this month.\n"
    "- **Salary Beans** = 100% of Local + 50% of Overseas.\n"
    "- **S6 Qualify**: Salary Beans ≥ 600,000.\n"
    "- **S6 Bonus**: $200 per qualifying host if ≥ 10% reach S6 *and* you have > 10 hosts."
)

uploaded = st.file_uploader(
    "📂 Upload host data (CSV/Excel) with columns: Host, Local Beans, Overseas Beans",
    type=["csv", "xlsx"]
)

def calculate_pay(df):
    df['Local Beans'] = pd.to_numeric(df['Local Beans'], errors='coerce').fillna(0)
    df['Overseas Beans'] = pd.to_numeric(df['Overseas Beans'], errors='coerce').fillna(0)
    df['Salary Beans'] = df['Local Beans'] + 0.5 * df['Overseas Beans']
    df['S6 Qualify'] = df['Salary Beans'] >= 600_000
    return df

if uploaded:
    if uploaded.name.endswith(".csv"):
        raw = pd.read_csv(uploaded)
    else:
        raw = pd.read_excel(uploaded)

    dfp = calculate_pay(raw)
    total = len(dfp)
    s6 = dfp['S6 Qualify'].sum()

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Hosts", total, "👥")
    c2.metric("Hosts ≥ S6", s6, "⭐")
    bonus = 0
    if total > 10 and s6/total >= 0.10:
        bonus = 200 * s6
        c3.metric("S6 Bonus", f"${bonus}", "💰")
    else:
        c3.metric("S6 Bonus", "Not Qualified", "❌")

    # Highlight table
    def hl(row):
        return ['background-color: lightgreen' if row['S6 Qualify'] else '' for _ in row]
    st.dataframe(dfp.style.apply(hl, axis=1), use_container_width=True)

    @st.cache_data
    def to_excel(df):
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Pay_Calc")
        return buf.getvalue()

    xl = to_excel(dfp)
    st.download_button(
        "📥 Download Host Pay Results (Excel)",
        data=xl,
        file_name=f"host_pay_{datetime.now():%Y%m%d}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.warning("Please upload a host data file to calculate pays.")
