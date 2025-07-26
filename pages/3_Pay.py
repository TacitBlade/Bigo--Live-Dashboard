import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="💸 Pay Sheet", layout="wide")
st.title("💸 Host Pay Sheet Calculator")

st.info("💰 Calculate host payouts based on PK performance, agency rules, and bonuses.")

# Sample host data with performance metrics
hosts_data = {
    "Host Name": ["prinny_x", "lisalush", "crazybitch", "hostess_anna", "star_player", "pk_master"],
    "PK Wins": [15, 22, 8, 18, 25, 12],
    "PK Losses": [8, 5, 15, 7, 3, 11],
    "Total Matches": [23, 27, 23, 25, 28, 23],
    "Win Rate (%)": [65.2, 81.5, 34.8, 72.0, 89.3, 52.2],
    "Total Beans Earned": [125000, 180000, 85000, 145000, 220000, 95000],
    "Hours Streamed": [45, 52, 38, 48, 58, 42],
    "Agency Tier": ["Gold", "Platinum", "Silver", "Gold", "Platinum", "Silver"]
}

df_hosts = pd.DataFrame(hosts_data)

# Payment calculation settings
st.sidebar.header("💼 Payment Settings")

# Agency tier multipliers
tier_multipliers = {
    "Platinum": st.sidebar.slider("Platinum Tier Multiplier", 1.0, 2.0, 1.5),
    "Gold": st.sidebar.slider("Gold Tier Multiplier", 1.0, 2.0, 1.3),
    "Silver": st.sidebar.slider("Silver Tier Multiplier", 1.0, 2.0, 1.1)
}

# Base rates
base_win_bonus = st.sidebar.number_input("Base Win Bonus ($)", min_value=1, max_value=100, value=10)
base_hour_rate = st.sidebar.number_input("Base Hourly Rate ($)", min_value=1, max_value=50, value=15)
beans_conversion_rate = st.sidebar.number_input("Beans to $ Rate (per 1000)", min_value=0.01, max_value=1.0, value=0.1, step=0.01)

# Win rate bonuses
high_win_rate_bonus = st.sidebar.number_input("High Win Rate Bonus (>80%)", min_value=0, max_value=500, value=100)
medium_win_rate_bonus = st.sidebar.number_input("Medium Win Rate Bonus (>70%)", min_value=0, max_value=300, value=50)

# Calculate payments
def calculate_payment(row):
    tier_mult = tier_multipliers[row["Agency Tier"]]
    
    # Base calculations
    win_bonus = row["PK Wins"] * base_win_bonus * tier_mult
    hour_payment = row["Hours Streamed"] * base_hour_rate * tier_mult
    beans_payment = (row["Total Beans Earned"] / 1000) * beans_conversion_rate
    
    # Win rate bonuses
    win_rate_bonus = 0
    if row["Win Rate (%)"] > 80:
        win_rate_bonus = high_win_rate_bonus
    elif row["Win Rate (%)"] > 70:
        win_rate_bonus = medium_win_rate_bonus
    
    total_payment = win_bonus + hour_payment + beans_payment + win_rate_bonus
    
    return {
        "Win Bonus": round(win_bonus, 2),
        "Hour Payment": round(hour_payment, 2),
        "Beans Payment": round(beans_payment, 2),
        "Win Rate Bonus": round(win_rate_bonus, 2),
        "Total Payment": round(total_payment, 2)
    }

# Apply calculations
payment_details = df_hosts.apply(calculate_payment, axis=1, result_type='expand')
final_df = pd.concat([df_hosts, payment_details], axis=1)

# Display results
st.subheader("📊 Host Performance & Payment Overview")

# Summary metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_payout = final_df["Total Payment"].sum()
    st.metric("Total Payout", f"${total_payout:,.2f}")

with col2:
    avg_payout = final_df["Total Payment"].mean()
    st.metric("Average Payout", f"${avg_payout:,.2f}")

with col3:
    top_earner = final_df.loc[final_df["Total Payment"].idxmax(), "Host Name"]
    st.metric("Top Earner", top_earner)

with col4:
    total_matches = final_df["Total Matches"].sum()
    st.metric("Total Matches", total_matches)

# Filter options
st.subheader("🔍 Filter Options")
filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    selected_hosts = st.multiselect(
        "Select Hosts:", 
        options=final_df["Host Name"].tolist(),
        default=final_df["Host Name"].tolist()
    )

with filter_col2:
    selected_tiers = st.multiselect(
        "Select Agency Tiers:",
        options=final_df["Agency Tier"].unique().tolist(),
        default=final_df["Agency Tier"].unique().tolist()
    )

# Apply filters
filtered_df = final_df[
    (final_df["Host Name"].isin(selected_hosts)) & 
    (final_df["Agency Tier"].isin(selected_tiers))
]

# Display main table
st.subheader("💰 Detailed Payment Breakdown")

# Format the dataframe for better display
display_columns = [
    "Host Name", "Agency Tier", "PK Wins", "Win Rate (%)", 
    "Hours Streamed", "Total Beans Earned", "Win Bonus", 
    "Hour Payment", "Beans Payment", "Win Rate Bonus", "Total Payment"
]

display_df = filtered_df[display_columns].copy()

# Style the dataframe
def highlight_top_performers(s):
    is_top = s == s.max()
    return ['background-color: #90EE90' if v else '' for v in is_top]

def color_by_tier(row):
    if row["Agency Tier"] == "Platinum":
        return ['background-color: #E6E6FA'] * len(row)
    elif row["Agency Tier"] == "Gold":
        return ['background-color: #FFFACD'] * len(row)
    else:  # Silver
        return ['background-color: #F0F8FF'] * len(row)

styled_df = display_df.style.apply(highlight_top_performers, subset=["Total Payment"])\
                              .apply(color_by_tier, axis=1)\
                              .format({
                                  "Win Rate (%)": "{:.1f}%",
                                  "Total Beans Earned": "{:,}",
                                  "Win Bonus": "${:.2f}",
                                  "Hour Payment": "${:.2f}",
                                  "Beans Payment": "${:.2f}",
                                  "Win Rate Bonus": "${:.2f}",
                                  "Total Payment": "${:.2f}"
                              })

st.dataframe(styled_df, use_container_width=True, height=400)

# Payment analysis
st.subheader("📈 Payment Analysis")

analysis_col1, analysis_col2 = st.columns(2)

with analysis_col1:
    # Top performers chart
    st.write("**Top 3 Earners**")
    top_3 = filtered_df.nlargest(3, "Total Payment")[["Host Name", "Total Payment"]]
    for idx, (_, row) in enumerate(top_3.iterrows(), 1):
        st.write(f"{idx}. {row['Host Name']}: ${row['Total Payment']:,.2f}")

with analysis_col2:
    # Payment breakdown pie chart
    st.write("**Payment Sources Breakdown**")
    payment_sources = {
        "Win Bonuses": filtered_df["Win Bonus"].sum(),
        "Hour Payments": filtered_df["Hour Payment"].sum(),
        "Beans Payments": filtered_df["Beans Payment"].sum(),
        "Win Rate Bonuses": filtered_df["Win Rate Bonus"].sum()
    }
    
    for source, amount in payment_sources.items():
        percentage = (amount / total_payout) * 100
        st.write(f"• {source}: ${amount:,.2f} ({percentage:.1f}%)")

# Export functionality
st.subheader("📥 Export Options")
export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    if st.button("📊 Export Full Report"):
        csv_data = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=f"host_payments_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with export_col2:
    if st.button("💼 Export Summary"):
        summary_data = filtered_df[["Host Name", "Agency Tier", "Total Payment"]].to_csv(index=False)
        st.download_button(
            label="Download Summary CSV",
            data=summary_data,
            file_name=f"payment_summary_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with export_col3:
    if st.button("🔄 Refresh Calculations"):
        st.rerun()

# Notes and recommendations
st.markdown("---")
st.subheader("💡 Payment Insights")

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.markdown("**🎯 Performance Insights:**")
    avg_win_rate = filtered_df["Win Rate (%)"].mean()
    high_performers = len(filtered_df[filtered_df["Win Rate (%)"] > 75])
    st.write(f"• Average win rate: {avg_win_rate:.1f}%")
    st.write(f"• High performers (>75% win rate): {high_performers}")
    st.write(f"• Total streaming hours: {filtered_df['Hours Streamed'].sum()}")

with insights_col2:
    st.markdown("**💰 Payment Insights:**")
    tier_distribution = filtered_df["Agency Tier"].value_counts()
    st.write("• Tier distribution:")
    for tier, count in tier_distribution.items():
        avg_payment = filtered_df[filtered_df["Agency Tier"] == tier]["Total Payment"].mean()
        st.write(f"  - {tier}: {count} hosts (avg: ${avg_payment:.2f})")

st.info("🚀 **Coming Soon:** Integration with `paysheet.py` for automated calculations and direct payment processing.")
