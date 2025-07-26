import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="📅 PK Schedule", layout="wide")
st.title("📅 Weekly PK Schedule")

st.info("🗓️ This section shows the weekly PK schedule for hosts. Data can be synced with Google Sheets in future updates.")

# Create dynamic schedule data
current_date = datetime.now()
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Sample dynamic schedule with more hosts and realistic data
schedule_data = {
    "Host": ["prinny_x", "lisalush", "crazybitch", "hostess_anna", "star_player", "pk_master"],
    "Monday": ["Talent PK 8PM", "Family 2v2 7PM", "Mini PK 9PM", "Rest", "Agency Battle 6PM", "Solo Stream"],
    "Tuesday": ["Rest", "Agency vs Agency 8PM", "Family Team 7PM", "Talent PK 9PM", "Rest", "Group PK 8:30PM"],
    "Wednesday": ["Talent Challenge 7:30PM", "Family Wars 8PM", "Agency Battle 6:30PM", "Mini PK 8PM", "Solo Stream", "Rest"],
    "Thursday": ["Family 2v2 8PM", "Rest", "Talent vs Agency 7PM", "Rest", "PK Challenge 9PM", "Family Team 7:30PM"],
    "Friday": ["Weekend Special 8PM", "Group Battle 7:30PM", "Agency Wars 8:30PM", "Family PK 7PM", "Talent Show 9PM", "Mini Battle 8PM"],
    "Saturday": ["Rest", "Weekend Marathon 6PM", "Family Special 8PM", "Agency Challenge 7:30PM", "Rest", "Group Wars 9PM"],
    "Sunday": ["Prep Day", "Family Time 7PM", "Rest", "Talent Review 8PM", "Agency Meeting", "Rest"]
}

df_schedule = pd.DataFrame(schedule_data)

# Display current week info
st.subheader(f"📅 Week of {current_date.strftime('%B %d, %Y')}")

# Add filters
col1, col2 = st.columns(2)
with col1:
    show_hosts = st.multiselect(
        "🎭 Filter by Host:", 
        options=df_schedule["Host"].tolist(),
        default=df_schedule["Host"].tolist()
    )

with col2:
    show_days = st.multiselect(
        "📆 Filter by Day:",
        options=weekdays,
        default=weekdays
    )

# Filter the schedule
filtered_schedule = df_schedule[df_schedule["Host"].isin(show_hosts)]
columns_to_show = ["Host"] + [day for day in show_days if day in df_schedule.columns]
filtered_schedule = filtered_schedule[columns_to_show]

# Display the schedule table with styling
st.markdown("### 🏆 PK Schedule Overview")

# Color-code different types of events
def style_schedule(val):
    if pd.isna(val) or val == "Rest":
        return 'background-color: #f0f0f0; color: gray'
    elif "Talent" in val:
        return 'background-color: #e8f4fd; color: #1f77b4'
    elif "Family" in val:
        return 'background-color: #e8f5e8; color: #2ca02c'
    elif "Agency" in val:
        return 'background-color: #fff2cc; color: #ff7f0e'
    elif "Group" in val or "Battle" in val:
        return 'background-color: #ffe6e6; color: #d62728'
    else:
        return 'background-color: white'

# Apply styling and display
styled_df = filtered_schedule.style.applymap(style_schedule)
st.dataframe(styled_df, use_container_width=True, height=400)

# Legend
st.markdown("### 📋 Event Types Legend")
legend_col1, legend_col2, legend_col3, legend_col4 = st.columns(4)

with legend_col1:
    st.markdown("🎯 **Talent PK** - Individual skill challenges")
with legend_col2:
    st.markdown("👨‍👩‍👧‍👦 **Family PK** - Team-based competitions")
with legend_col3:
    st.markdown("🏢 **Agency PK** - Inter-agency battles")
with legend_col4:
    st.markdown("⚔️ **Group/Battle** - Multi-participant events")

# Statistics section
st.markdown("### 📊 Weekly Statistics")
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    total_events = sum(df_schedule.iloc[:, 1:].apply(lambda x: sum(x != "Rest") + sum(x != "Prep Day") + sum(x != "Prep") for x in x).sum())
    st.metric("Total Events", total_events)

with stat_col2:
    active_hosts = len([host for idx, row in df_schedule.iterrows() 
                       if any(val not in ["Rest", "Prep Day", "Prep"] for val in row.iloc[1:])])
    st.metric("Active Hosts", active_hosts)

with stat_col3:
    # Count rest days
    rest_count = sum(df_schedule.iloc[:, 1:].apply(lambda x: sum(x == "Rest")).sum())
    st.metric("Total Rest Slots", rest_count)

with stat_col4:
    # Average events per host
    avg_events = total_events / len(df_schedule) if len(df_schedule) > 0 else 0
    st.metric("Avg Events/Host", f"{avg_events:.1f}")

# Action buttons
st.markdown("### ⚙️ Schedule Management")
action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("📥 Export Schedule"):
        csv = filtered_schedule.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"pk_schedule_{current_date.strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with action_col2:
    if st.button("🔄 Refresh Data"):
        st.rerun()

with action_col3:
    if st.button("📋 Copy to Clipboard"):
        st.info("💡 Use the export button to download the schedule data.")

# Future integration note
st.markdown("---")
st.info("🚀 **Coming Soon:** Direct Google Sheets integration for real-time schedule updates and collaborative editing.")
