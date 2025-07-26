import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="💸 Pay & Chart", layout="wide")
st.title("💸 Pay & Chart Dashboard")

# Create two tabs: Host Pay and Pay Chart Viewer
tab1, tab2 = st.tabs(["👥 Host Pay Calculator", "📊 Pay Chart Viewer"])

# --- Tab 1: Host Pay Calculator ---
with tab1:
    st.header("👥 Host Pay Calculator")
    st.markdown("Use this tool to calculate host salary beans and bonuses under the Streamer Plan Policy effective March 1, 2025.")
    st.markdown(
        "- Enter each host's **Local Beans** and **Overseas Beans** earned this month.\n"
        "- **Salary Beans** = 100% of Local + 50% of Overseas.\n"
        "- **S6 Qualify**: Salary Beans ≥ 600,000.\n"
        "- **S6 Bonus**: $200 per qualifying host if ≥ 10% reach S6 *and* you have > 10 hosts."
    )

    uploaded = st.file_uploader(
        "📂 Upload host data (CSV/Excel) with columns: Host, Local Beans, Overseas Beans",
        type=["csv", "xlsx"], key="host_pay_upload"
    )

    def calculate_pay(df):
        df['Local Beans'] = pd.to_numeric(df['Local Beans'], errors='coerce').fillna(0)
        df['Overseas Beans'] = pd.to_numeric(df['Overseas Beans'], errors='coerce').fillna(0)
        df['Salary Beans'] = df['Local Beans'] + 0.5 * df['Overseas Beans']
        df['S6 Qualify'] = df['Salary Beans'] >= 600_000
        return df

    if uploaded:
        if uploaded.name.endswith('.csv'):
            host_df = pd.read_csv(uploaded)
        else:
            host_df = pd.read_excel(uploaded)

        required_columns = ['Local Beans', 'Overseas Beans']
        if not all(col in host_df.columns for col in required_columns):
            st.error(
                "The uploaded file is missing required columns. "
                f"Please ensure it has: {', '.join(required_columns)}"
            )
        else:
            host_df = calculate_pay(host_df)
            total = len(host_df)
            s6_count = host_df['S6 Qualify'].sum()

            c1, c2, c3 = st.columns(3)
            c1.metric("Total Hosts", total, "👥")
            c2.metric("Hosts ≥ S6", int(s6_count), "🌟")
            bonus_amt = 0
            if total > 10 and s6_count / total >= 0.10:
                bonus_amt = 200 * int(s6_count)
                c3.metric("S6 Bonus", f"${bonus_amt}", "💰")
            else:
                c3.metric("S6 Bonus", "Not Qualified", "❌")

            # Highlight rows
            def hl_s6(row):
                return ['background-color: lightgreen' if row['S6 Qualify'] else '' for _ in row]
            st.dataframe(host_df.style.apply(hl_s6, axis=1), use_container_width=True)

            @st.cache_data
            def to_excel(df):
                buf = BytesIO()
                with pd.ExcelWriter(buf, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Pay_Calc')
                return buf.getvalue()

            excel_data = to_excel(host_df)
            st.download_button(
                "📥 Download Host Pay Results (Excel)",
                data=excel_data,
                file_name=f"host_pay_{datetime.now():%Y%m%d}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.warning("Please upload a host data file to calculate pays.")

# --- Tab 2: Pay Chart Viewer ---
with tab2:
    st.header("📊 Pay Chart Viewer")
    st.markdown(
        "This viewer loads the pay chart from the agency's Excel reference file."
    )
    # Load the pay chart Excel file
    try:
        chart_df = pd.read_excel(
            'templates/Alpha_Omega_Agency_Pay_Chart_with_Diamonds.xlsx'
        )
        # Drop unwanted columns
        to_drop = ['Effective Broadcasting Limit (Hours)', 'Billable hours limit (hours/day)']
        existing = [col for col in to_drop if col in chart_df.columns]
        chart_df = chart_df.drop(columns=existing)

        # Filtering controls
        st.subheader("Filters")
        filtered_df = chart_df.copy()
        for col in chart_df.columns:
            options = ['All'] + sorted(chart_df[col].dropna().unique().tolist())
            selected = st.selectbox(f"Filter by {col}", options)
            if selected != 'All':
                filtered_df = filtered_df[filtered_df[col] == selected]

        st.subheader("Pay Chart")
        st.dataframe(filtered_df, use_container_width=True)

        # Export button
        @st.cache_data
        def to_excel_chart(df):
            buf = BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Pay_Chart')
            return buf.getvalue()

        excel_chart = to_excel_chart(filtered_df)
        st.download_button(
            "📥 Download Pay Chart (Excel)",
            data=excel_chart,
            file_name=f"pay_chart_{datetime.now():%Y%m%d}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except FileNotFoundError:
        st.error("Pay chart file not found. Please ensure 'templates/Alpha_Omega_Agency_Pay_Chart_with_Diamonds.xlsx' is in your project directory.")
