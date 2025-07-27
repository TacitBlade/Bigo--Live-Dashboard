import streamlit as st
import pandas as pd
from utils.gsheets import read_filtered_columns
from utils.gsheets_writer import write_dataframe_to_sheet
from utils.data_validator import safe_date_conversion, clean_text_data, display_data_info
from datetime import timedelta
import time

# Load custom CSS
def load_css():
    css_files = ['static/enhanced_style.css', 'static/style.css']
    for css_file in css_files:
        try:
            with open(css_file) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
                break  # Use the first available CSS file
        except FileNotFoundError:
            continue

# ---- Config ----
st.set_page_config(page_title="Bigo Agency Dashboard", page_icon="🎥", layout="wide")

# Load CSS
load_css()

# Navigation
st.sidebar.title("🏠 Navigation")
page = st.sidebar.selectbox("Choose a page:", ["Home", "PK Viewer", "Schedule", "Pay", "Diamond Calculator", "Host Pay Calculator"])

# Ensure the selectbox reflects the current page
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# Update session state when page changes
if page != st.session_state.current_page:
    st.session_state.current_page = page

if st.session_state.current_page == "Home":
    # Landing page content
    st.title("🎥 Welcome to the Bigo Agency Dashboard")
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin: 2rem 0;">
        <h2 style="color: white; margin: 0;">Your Complete Agency Management Solution</h2>
        <p style="color: white; font-size: 1.2rem; margin: 1rem 0;">Streamline your Bigo Live agency operations with powerful tools and insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="padding: 1.5rem; border: 1px solid #ddd; border-radius: 8px; height: 200px;">
            <h3>📊 PK Viewer</h3>
            <p>View and manage PK data from multiple sheets. Filter, search, and export your data with ease.</p>
            <ul>
                <li>Real-time data loading</li>
                <li>Advanced filtering</li>
                <li>Export to Excel</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="padding: 1.5rem; border: 1px solid #ddd; border-radius: 8px; height: 200px;">
            <h3>📅 Schedule</h3>
            <p>Manage your agency's scheduling needs and keep track of important events and deadlines.</p>
            <ul>
                <li>Event management</li>
                <li>Calendar integration</li>
                <li>Automated reminders</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="padding: 1.5rem; border: 1px solid #ddd; border-radius: 8px; height: 200px;">
            <h3>💰 Pay & Calculator</h3>
            <p>Handle payments and calculate earnings with our integrated financial tools.</p>
            <ul>
                <li>Payment tracking</li>
                <li>Diamond calculations</li>
                <li>Financial reports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick stats section
    st.markdown("---")
    st.subheader("📈 Quick Stats")
    
    # Load basic stats for the landing page
    try:
        # Load minimal data for stats
        sheet_urls = {
            "Training PKs": "https://docs.google.com/spreadsheets/d/1T2Za-VeqUe4hN-00X-Qa5T3FAgXMExz2B1Brhspbr7w/edit?gid=920344037",
            "Tasks": "https://docs.google.com/spreadsheets/d/1DD7I5sMu55wRVwGjPEv43iygq2b8oudfMspGlOY1zck/edit?gid=1990132269",
            "Mystery Matches": "https://docs.google.com/spreadsheets/d/1iS9acwW9DrjZQh_d51_Pv4DcN9_X4alzK3wC2KIWXYw/edit?gid=1234468340",
        }
        
        total_records = 0
        sheets_loaded = 0
        
        for name, url in sheet_urls.items():
            try:
                df = read_filtered_columns(url)
                if not df.empty:
                    total_records += len(df)
                    sheets_loaded += 1
            except:
                continue
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Total Records", f"{total_records:,}")
        with col2:
            st.metric("📋 Active Sheets", sheets_loaded)
        with col3:
            st.metric("🔄 Status", "Online" if sheets_loaded > 0 else "Offline")
        with col4:
            st.metric("⏰ Last Updated", "Just now")
            
    except Exception as e:
        st.info("📊 Stats will appear here once data is loaded")
    
    # Getting started section
    st.markdown("---")
    st.subheader("🚀 Getting Started")
    st.markdown("""
    1. **Select a page** from the sidebar navigation
    2. **PK Viewer** - Start here to view and manage your PK data
    3. **Schedule** - Manage your agency's calendar and events
    4. **Pay** - Handle payments and financial calculations
    5. **Diamond Calculator** - Calculate diamond values and earnings
    """)
    
    # Quick actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Go to PK Viewer", use_container_width=True):
            st.session_state.current_page = "PK Viewer"
            st.rerun()
    with col2:
        if st.button("📅 View Schedule", use_container_width=True):
            st.session_state.current_page = "Schedule"  
            st.rerun()
    with col3:
        if st.button("💰 Access Pay Tools", use_container_width=True):
            st.session_state.current_page = "Pay"
            st.rerun()

elif st.session_state.current_page == "PK Viewer":
    st.title("📊 PK Data Viewer")
    
    # --- Auto Refresh and Cache Management ---
    col1, col2 = st.sidebar.columns(2)

    with col1:
        refresh_interval = st.selectbox("🔄 Auto-refresh every...", [0, 1, 2, 5, 10], index=0)

    with col2:
        if st.button("🗑️ Clear Cache"):
            st.cache_data.clear()
            st.success("Cache cleared!")
            st.rerun()

    refresh_interval = st.slider("Auto-refresh interval (seconds)", 30, 300, 60)
if st.button("Enable Auto-Refresh"):
    while True:
        st.rerun()
        time.sleep(refresh_interval)
        
        current_time = time.time()
        if current_time - st.session_state.last_refresh > refresh_interval * 60:
            st.session_state.last_refresh = current_time
            st.rerun()

    # --- Load sheets ---
    sheet_urls = {
        "Sheet 1": "https://docs.google.com/spreadsheets/d/1T2Za-VeqUe4hN-00X-Qa5T3FAgXMExz2B1Brhspbr7w/edit?gid=920344037",
        "Sheet 2": "https://docs.google.com/spreadsheets/d/1DD7I5sMu55wRVwGjPEv43iygq2b8oudfMspGlOY1zck/edit?gid=1990132269",
        "Sheet 3": "https://docs.google.com/spreadsheets/d/1iS9acwW9DrjZQh_d51_Pv4DcN9_X4alzK3wC2KIWXYw/edit?gid=1234468340",
    }
    sheet_map = {
        "Training PKs": "https://docs.google.com/spreadsheets/d/1T2Za-VeqUe4hN-00X-Qa5T3FAgXMExz2B1Brhspbr7w/edit?gid=920344037",
        "Tasks": "https://docs.google.com/spreadsheets/d/1DD7I5sMu55wRVwGjPEv43iygq2b8oudfMspGlOY1zck/edit?gid=1990132269",
        "Mystery Matches": "https://docs.google.com/spreadsheets/d/1iS9acwW9DrjZQh_d51_Pv4DcN9_X4alzK3wC2KIWXYw/edit?gid=1234468340",
    }

    selected_sheet_name = st.sidebar.selectbox("📋 Select PK Sheet", options=sheet_map.keys())
    selected_sheet_url = sheet_map[selected_sheet_name]

    @st.cache_data(ttl=300)
    def load_all_data() -> pd.DataFrame:
        all_dfs = []
        for name, url in sheet_urls.items():
            try:
                df = read_filtered_columns(url)
                if not df.empty:
                    df["Source Sheet"] = name
                    all_dfs.append(df)
            except Exception as e:
                st.warning(f"⚠️ Could not load {name}: {str(e)}")
        
        if all_dfs:
            return pd.concat(all_dfs, ignore_index=True)
        else:
            return pd.DataFrame()

    # Load the combined data
    combined_df = load_all_data()

    # Clean and validate the data
    if not combined_df.empty:
        combined_df = clean_text_data(combined_df)
        combined_df = safe_date_conversion(combined_df)

    # Display data info
    if not combined_df.empty:
        display_data_info(combined_df, "Combined Data Summary")

    # --- Sidebar filters ---
    st.sidebar.header("🔍 Filter Data")

    # Quick date filters
    if not combined_df.empty and "Date" in combined_df.columns:
        today = pd.Timestamp.now().normalize()
        this_week = today - timedelta(days=today.weekday())

        quick_filter = st.sidebar.radio("📅 Quick Filter", ["All", "Today", "This Week"])

        if quick_filter == "Today":
            combined_df = combined_df[combined_df["Date"].dt.date == today.date()]
        elif quick_filter == "This Week":
            combined_df = combined_df[(combined_df["Date"] >= this_week) & (combined_df["Date"] <= today + timedelta(days=1))]
    else:
        st.sidebar.info("📋 No data available for date filtering")

    # Regular filters
    if not combined_df.empty:
        if "Date" in combined_df.columns:
            date_options = sorted(combined_df["Date"].dropna().dt.strftime("%Y-%m-%d").unique())
        else:
            date_options = []
        
        if "Agency Name.1" in combined_df.columns:
            agency1_options = sorted(combined_df["Agency Name.1"].dropna().unique())
        else:
            agency1_options = []
        
        if "Agency Name.2" in combined_df.columns:
            agency2_options = sorted(combined_df["Agency Name.2"].dropna().unique())
        else:
            agency2_options = []
    else:
        date_options = []
        agency1_options = []
        agency2_options = []

    selected_date = st.sidebar.multiselect("Select Date", date_options, default=date_options)
    selected_agency1 = st.sidebar.multiselect("Agency Name 1", agency1_options, default=agency1_options)
    selected_agency2 = st.sidebar.multiselect("Agency Name 2", agency2_options, default=agency2_options)

    # Search box
    search_text = st.text_input("🔎 Search any keyword (ID, Agency, Date, etc.)")

    # Apply filters
    if not combined_df.empty:
        filtered_df = combined_df.copy()
        
        # Apply date filter
        if selected_date and "Date" in combined_df.columns:
            filtered_df = filtered_df[filtered_df["Date"].dt.strftime("%Y-%m-%d").isin(selected_date)]
        
        # Apply agency filters
        if selected_agency1 and "Agency Name.1" in combined_df.columns:
            filtered_df = filtered_df[filtered_df["Agency Name.1"].isin(selected_agency1)]
        
        if selected_agency2 and "Agency Name.2" in combined_df.columns:
            filtered_df = filtered_df[filtered_df["Agency Name.2"].isin(selected_agency2)]
    else:
        filtered_df = combined_df.copy()

    # Apply search
    if search_text and not filtered_df.empty:
        search_text = search_text.lower()
        mask = filtered_df.astype(str).apply(lambda x: x.str.lower().str.contains(search_text, na=False)).any(axis=1)
        filtered_df = filtered_df[mask]

    # Save to Google Sheet button (now filtered_df is defined)
    if st.button("✍️ Save back to Google Sheet"):
        if not filtered_df.empty:
            try:
                write_dataframe_to_sheet(
                    sheet_url=sheet_map[selected_sheet_name],
                    worksheet_name="StreamlitExport",
                    df=filtered_df
                )
                st.success("Sheet updated successfully ✅")
            except Exception as e:
                st.error(f"Error saving to sheet: {str(e)}")
        else:
            st.warning("No data to save!")

    st.success(f"✅ {len(filtered_df)} rows matched your filters.")

    # Display data if available
    if not filtered_df.empty:
        # --- Styled Table with Conditional Highlight ---
        def render_html_table(df: pd.DataFrame) -> str:
            html = "<style>td, th {padding: 6px 12px;} table {border-collapse: collapse; width: 100%; font-size: 15px;} th {background: #eee;}</style>"
            html += "<table border='1'>"
            html += "<thead><tr>" + "".join([f"<th>{col}</th>" for col in df.columns]) + "</tr></thead><tbody>"

            for idx, (_, row) in enumerate(df.iterrows()):
                # Highlight if agencies are the same
                bg_color = "#ffe5e5" if row.get("Agency Name.1") == row.get("Agency Name.2") else ("#f9f9f9" if idx % 2 == 0 else "#ffffff")
                html += f"<tr style='background-color:{bg_color}'>" + "".join(
                    [f"<td>{str(cell)}</td>" for cell in row]) + "</tr>"
            html += "</tbody></table>"
            return html

        st.markdown(render_html_table(filtered_df), unsafe_allow_html=True)
    else:
        st.warning("⚠️ No data available or no matches found with current filters.")

    # --- Download to Excel ---
    @st.cache_data
    def convert_to_excel(df: pd.DataFrame) -> bytes:
        import io
        output = io.BytesIO()
        try:
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name="PK Data")
            return output.getvalue()
        except Exception as e:
            st.error(f"Error creating Excel file: {str(e)}")
            return b""

    if not filtered_df.empty:
        excel_data = convert_to_excel(filtered_df)
        if excel_data:
            st.download_button(
                label="📥 Download Filtered Data (Excel)",
                data=excel_data,
                file_name="bigo_pk_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

elif st.session_state.current_page == "Host Pay Calculator":
    st.title("🧮 Host Pay Calculator")
    
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #28a745 0%, #20c997 100%); border-radius: 10px; margin: 1rem 0;">
        <h3 style="color: white; margin: 0;">💰 Calculate Host Earnings</h3>
        <p style="color: white; margin: 0.5rem 0;">Determine host payments based on performance metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Performance Metrics")
        
        # Basic inputs
        diamonds_earned = st.number_input("💎 Diamonds Earned", min_value=0, value=0, step=100)
        hours_streamed = st.number_input("⏰ Hours Streamed", min_value=0.0, value=0.0, step=0.5)
        pk_wins = st.number_input("🏆 PK Wins", min_value=0, value=0, step=1)
        pk_losses = st.number_input("❌ PK Losses", min_value=0, value=0, step=1)
        
        # Additional metrics
        st.subheader("🎯 Bonus Metrics")
        daily_tasks_completed = st.number_input("✅ Daily Tasks Completed", min_value=0, value=0, step=1)
        special_events = st.number_input("🎉 Special Events Participated", min_value=0, value=0, step=1)
        
    with col2:
        st.subheader("💰 Pay Structure")
        
        # Pay rates
        base_rate_per_hour = st.number_input("💵 Base Rate per Hour ($)", min_value=0.0, value=5.0, step=0.5)
        diamond_rate = st.number_input("💎 Rate per 1000 Diamonds ($)", min_value=0.0, value=1.0, step=0.1)
        pk_win_bonus = st.number_input("🏆 PK Win Bonus ($)", min_value=0.0, value=2.0, step=0.5)
        task_bonus = st.number_input("✅ Task Completion Bonus ($)", min_value=0.0, value=1.0, step=0.25)
        event_bonus = st.number_input("🎉 Event Participation Bonus ($)", min_value=0.0, value=5.0, step=1.0)
        
        # Deductions
        st.subheader("📉 Deductions")
        pk_loss_penalty = st.number_input("❌ PK Loss Penalty ($)", min_value=0.0, value=0.5, step=0.25)
        other_deductions = st.number_input("🔻 Other Deductions ($)", min_value=0.0, value=0.0, step=0.5)
    
    # Calculate earnings
    if st.button("🧮 Calculate Pay", use_container_width=True):
        # Base calculations
        base_pay = hours_streamed * base_rate_per_hour
        diamond_earnings = (diamonds_earned / 1000) * diamond_rate
        pk_bonus = pk_wins * pk_win_bonus
        task_earnings = daily_tasks_completed * task_bonus
        event_earnings = special_events * event_bonus
        
        # Deductions
        pk_penalties = pk_losses * pk_loss_penalty
        total_deductions = pk_penalties + other_deductions
        
        # Total calculation
        gross_pay = base_pay + diamond_earnings + pk_bonus + task_earnings + event_earnings
        net_pay = gross_pay - total_deductions
        
        # Display results
        st.markdown("---")
        st.subheader("💰 Payment Breakdown")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 Earnings")
            st.metric("Base Pay", f"${base_pay:.2f}")
            st.metric("Diamond Earnings", f"${diamond_earnings:.2f}")
            st.metric("PK Win Bonus", f"${pk_bonus:.2f}")
            st.metric("Task Bonus", f"${task_earnings:.2f}")
            st.metric("Event Bonus", f"${event_earnings:.2f}")
            
        with col2:
            st.markdown("### 📉 Deductions")
            st.metric("PK Loss Penalty", f"${pk_penalties:.2f}")
            st.metric("Other Deductions", f"${other_deductions:.2f}")
            st.metric("Total Deductions", f"${total_deductions:.2f}")
            
        with col3:
            st.markdown("### 💵 Final Pay")
            st.metric("Gross Pay", f"${gross_pay:.2f}")
            st.metric("Net Pay", f"${net_pay:.2f}", delta=f"${net_pay - gross_pay:.2f}")
            
            # Performance indicators
            if pk_wins > 0:
                win_rate = (pk_wins / (pk_wins + pk_losses)) * 100 if (pk_wins + pk_losses) > 0 else 0
                st.metric("PK Win Rate", f"{win_rate:.1f}%")
        
        # Detailed breakdown table
        st.markdown("---")
        st.subheader("📋 Detailed Breakdown")
        
        breakdown_data = {
            "Category": ["Base Pay", "Diamond Earnings", "PK Win Bonus", "Task Bonus", "Event Bonus", "PK Loss Penalty", "Other Deductions"],
            "Amount ($)": [base_pay, diamond_earnings, pk_bonus, task_earnings, event_earnings, -pk_penalties, -other_deductions],
            "Details": [
                f"{hours_streamed} hours × ${base_rate_per_hour}/hour",
                f"{diamonds_earned:,} diamonds × ${diamond_rate}/1000",
                f"{pk_wins} wins × ${pk_win_bonus}",
                f"{daily_tasks_completed} tasks × ${task_bonus}",
                f"{special_events} events × ${event_bonus}",
                f"{pk_losses} losses × ${pk_loss_penalty}",
                f"Manual deduction"
            ]
        }
        
        breakdown_df = pd.DataFrame(breakdown_data)
        st.dataframe(breakdown_df, use_container_width=True)
        
        # Summary card
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, {'#28a745' if net_pay >= 0 else '#dc3545'} 0%, {'#20c997' if net_pay >= 0 else '#c82333'} 100%); border-radius: 10px; margin: 2rem 0;">
            <h2 style="color: white; margin: 0;">Final Payment: ${net_pay:.2f}</h2>
            <p style="color: white; font-size: 1.1rem; margin: 0.5rem 0;">
                {'✅ Payment Complete' if net_pay >= 0 else '⚠️ Review Required'}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Export option
        if st.button("📄 Export Calculation Report"):
            report_data = {
                "Host Pay Calculation Report": [""],
                "Date": [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")],
                "": [""],
                "Performance Metrics": [""],
                "Diamonds Earned": [diamonds_earned],
                "Hours Streamed": [hours_streamed],
                "PK Wins": [pk_wins],
                "PK Losses": [pk_losses],
                "Tasks Completed": [daily_tasks_completed],
                "Events Participated": [special_events],
                " ": [""],
                "Payment Breakdown": [""],
                "Base Pay": [f"${base_pay:.2f}"],
                "Diamond Earnings": [f"${diamond_earnings:.2f}"],
                "PK Bonus": [f"${pk_bonus:.2f}"],
                "Task Bonus": [f"${task_earnings:.2f}"],
                "Event Bonus": [f"${event_earnings:.2f}"],
                "Total Deductions": [f"${total_deductions:.2f}"],
                "  ": [""],
                "Final Payment": [f"${net_pay:.2f}"]
            }
            
            report_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in report_data.items()]))
            
            excel_data = convert_to_excel(report_df)
            if excel_data:
                st.download_button(
                    label="📥 Download Calculation Report",
                    data=excel_data,
                    file_name=f"host_pay_calculation_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

else:
    # Placeholder for other pages
    st.title(f"🚧 {st.session_state.current_page} Page")
    st.info(f"The {st.session_state.current_page} page is under construction. Please check back later!")
    st.markdown(f"### Coming Soon: {st.session_state.current_page} Features")
    
    if st.session_state.current_page == "Schedule":
        st.markdown("""
        - 📅 Calendar view
        - ⏰ Event scheduling
        - 🔔 Notifications
        - 📊 Schedule analytics
        """)
    elif st.session_state.current_page == "Pay":
        st.markdown("""
        - 💰 Payment processing
        - 📈 Earnings tracking
        - 💎 Diamond calculations
        - 📊 Financial reports
        """)
    elif st.session_state.current_page == "Diamond Calculator":
        st.markdown("""
        - 💎 Diamond value calculations
        - 💰 Currency conversions
        - 📊 Earning projections
        - 📈 Historical data
        """)
