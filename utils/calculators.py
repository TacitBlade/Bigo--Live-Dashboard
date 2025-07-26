"""
Calculators for various Bigo Live metrics and conversions.
Includes beans to diamonds conversion, PK calculations, and performance metrics.
"""

import streamlit as st
from typing import Dict

# Conversion rates (these should be configurable)
BEANS_TO_DIAMONDS_RATE = 210  # 210 beans = 1 diamond
DIAMOND_TO_USD_RATE = 0.005   # 1 diamond ≈ $0.005 USD

def beans_to_diamonds(beans: int) -> float:
    """Convert beans to diamonds."""
    return beans / BEANS_TO_DIAMONDS_RATE

def diamonds_to_beans(diamonds: float) -> int:
    """Convert diamonds to beans."""
    return int(diamonds * BEANS_TO_DIAMONDS_RATE)

def diamonds_to_usd(diamonds: float) -> float:
    """Convert diamonds to USD."""
    return diamonds * DIAMOND_TO_USD_RATE

def calculate_pk_performance(received_beans: int, sent_beans: int) -> Dict[str, float]:
    """Calculate PK performance metrics."""
    received_diamonds = beans_to_diamonds(received_beans)
    sent_diamonds = beans_to_diamonds(sent_beans)
    net_diamonds = received_diamonds - sent_diamonds
    net_usd = diamonds_to_usd(net_diamonds)
    
    efficiency = (received_diamonds / sent_diamonds * 100) if sent_beans > 0 else 0
    
    return {
        "received_diamonds": received_diamonds,
        "sent_diamonds": sent_diamonds,
        "net_diamonds": net_diamonds,
        "net_usd": net_usd,
        "efficiency_percent": efficiency
    }

def calculate_host_targets(monthly_target: float, days_worked: int, current_diamonds: float) -> Dict[str, float]:
    """Calculate host targets and progress."""
    days_in_month = 30  # Simplified
    daily_target = monthly_target / days_in_month
    expected_progress = daily_target * days_worked
    progress_percent = (current_diamonds / monthly_target * 100) if monthly_target > 0 else 0
    remaining_target = max(0, monthly_target - current_diamonds)
    days_remaining = days_in_month - days_worked
    daily_required = remaining_target / days_remaining if days_remaining > 0 else 0
    
    return {
        "daily_target": daily_target,
        "expected_progress": expected_progress,
        "progress_percent": progress_percent,
        "remaining_target": remaining_target,
        "daily_required": daily_required,
        "on_track": current_diamonds >= expected_progress
    }

def pk_calculator_widget():
    """Streamlit widget for PK calculations."""
    st.subheader("💎 PK Performance Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        received_beans = st.number_input("Beans Received", min_value=0, value=0, step=1000)
        sent_beans = st.number_input("Beans Sent", min_value=0, value=0, step=1000)
    
    with col2:
        if st.button("Calculate PK Performance"):
            results = calculate_pk_performance(received_beans, sent_beans)
            
            st.success("📊 **PK Performance Results:**")
            st.write(f"💎 Received: {results['received_diamonds']:.2f} diamonds")
            st.write(f"💎 Sent: {results['sent_diamonds']:.2f} diamonds")
            st.write(f"💎 Net: {results['net_diamonds']:.2f} diamonds")
            st.write(f"💵 Net USD: ${results['net_usd']:.2f}")
            st.write(f"📈 Efficiency: {results['efficiency_percent']:.1f}%")

def target_calculator_widget():
    """Streamlit widget for target calculations."""
    st.subheader("🎯 Host Target Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        monthly_target = st.number_input("Monthly Target (Diamonds)", min_value=0.0, value=10000.0, step=100.0)
    
    with col2:
        days_worked = st.number_input("Days Worked", min_value=0, max_value=31, value=15, step=1)
    
    with col3:
        current_diamonds = st.number_input("Current Diamonds", min_value=0.0, value=5000.0, step=100.0)
    
    if st.button("Calculate Target Progress"):
        results = calculate_host_targets(monthly_target, days_worked, current_diamonds)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("📊 **Target Analysis:**")
            st.write(f"🎯 Daily Target: {results['daily_target']:.0f} diamonds")
            st.write(f"📈 Progress: {results['progress_percent']:.1f}%")
            st.write(f"⏰ Expected by now: {results['expected_progress']:.0f}")
            
        with col2:
            status = "✅ On Track" if results['on_track'] else "⚠️ Behind Target"
            st.write(f"Status: {status}")
            st.write(f"🎯 Remaining: {results['remaining_target']:.0f} diamonds")
            st.write(f"📅 Daily Required: {results['daily_required']:.0f} diamonds")

def conversion_calculator_widget():
    """Streamlit widget for conversion calculations."""
    st.subheader("🔄 Conversion Calculator")
    
    tab1, tab2, tab3 = st.tabs(["Beans ➜ Diamonds", "Diamonds ➜ Beans", "Diamonds ➜ USD"])
    
    with tab1:
        beans = st.number_input("Beans", min_value=0, value=2100, step=100, key="beans_input")
        diamonds = beans_to_diamonds(beans)
        st.success(f"💎 {beans:,} beans = {diamonds:.2f} diamonds")
    
    with tab2:
        diamonds = st.number_input("Diamonds", min_value=0.0, value=10.0, step=0.1, key="diamonds_input")
        beans = diamonds_to_beans(diamonds)
        st.success(f"🫘 {diamonds:.2f} diamonds = {beans:,} beans")
    
    with tab3:
        diamonds = st.number_input("Diamonds", min_value=0.0, value=1000.0, step=10.0, key="diamonds_usd_input")
        usd = diamonds_to_usd(diamonds)
        st.success(f"💵 {diamonds:.0f} diamonds = ${usd:.2f} USD")
