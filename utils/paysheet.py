"""
Paysheet generation utilities for Bigo Live hosts.
Calculates payments based on performance metrics and agency rules.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# Default payment rules (should be configurable)
PAYMENT_RULES = {
    "base_rate": 0.4,  # 40% of diamonds earned
    "bonus_threshold": 10000,  # diamonds
    "bonus_rate": 0.1,  # additional 10% for exceeding threshold
    "pk_win_bonus": 500,  # diamonds bonus per PK win
    "attendance_bonus": 1000,  # diamonds bonus for perfect attendance
}

class HostPayment:
    """Class to handle individual host payment calculations."""
    
    def __init__(self, host_id: str, host_name: str):
        self.host_id = host_id
        self.host_name = host_name
        self.diamonds_earned = 0
        self.pk_wins = 0
        self.days_worked = 0
        self.target_days = 30
        self.additional_bonuses = 0
        self.deductions = 0
    
    def calculate_base_payment(self) -> float:
        """Calculate base payment from diamonds earned."""
        return self.diamonds_earned * PAYMENT_RULES["base_rate"]
    
    def calculate_performance_bonus(self) -> float:
        """Calculate performance-based bonus."""
        if self.diamonds_earned > PAYMENT_RULES["bonus_threshold"]:
            excess = self.diamonds_earned - PAYMENT_RULES["bonus_threshold"]
            return excess * PAYMENT_RULES["bonus_rate"]
        return 0
    
    def calculate_pk_bonus(self) -> float:
        """Calculate PK win bonus."""
        return self.pk_wins * PAYMENT_RULES["pk_win_bonus"]
    
    def calculate_attendance_bonus(self) -> float:
        """Calculate attendance bonus."""
        if self.days_worked >= self.target_days:
            return PAYMENT_RULES["attendance_bonus"]
        return 0
    
    def calculate_total_payment(self) -> Dict[str, float]:
        """Calculate total payment with breakdown."""
        base = self.calculate_base_payment()
        performance = self.calculate_performance_bonus()
        pk_bonus = self.calculate_pk_bonus()
        attendance = self.calculate_attendance_bonus()
        
        total_bonuses = performance + pk_bonus + attendance + self.additional_bonuses
        total_before_deductions = base + total_bonuses
        final_payment = total_before_deductions - self.deductions
        
        return {
            "base_payment": base,
            "performance_bonus": performance,
            "pk_bonus": pk_bonus,
            "attendance_bonus": attendance,
            "additional_bonuses": self.additional_bonuses,
            "total_bonuses": total_bonuses,
            "total_before_deductions": total_before_deductions,
            "deductions": self.deductions,
            "final_payment": max(0, final_payment)  # Ensure non-negative
        }

def generate_paysheet(hosts_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Generate paysheet DataFrame from hosts data."""
    paysheet_data = []
    
    for host_data in hosts_data:
        host = HostPayment(host_data["id"], host_data["name"])
        host.diamonds_earned = host_data.get("diamonds_earned", 0)
        host.pk_wins = host_data.get("pk_wins", 0)
        host.days_worked = host_data.get("days_worked", 0)
        host.additional_bonuses = host_data.get("additional_bonuses", 0)
        host.deductions = host_data.get("deductions", 0)
        
        payment_breakdown = host.calculate_total_payment()
        
        row = {
            "Host ID": host.host_id,
            "Host Name": host.host_name,
            "Diamonds Earned": host.diamonds_earned,
            "Days Worked": host.days_worked,
            "PK Wins": host.pk_wins,
            "Base Payment": payment_breakdown["base_payment"],
            "Performance Bonus": payment_breakdown["performance_bonus"],
            "PK Bonus": payment_breakdown["pk_bonus"],
            "Attendance Bonus": payment_breakdown["attendance_bonus"],
            "Additional Bonuses": payment_breakdown["additional_bonuses"],
            "Total Bonuses": payment_breakdown["total_bonuses"],
            "Deductions": payment_breakdown["deductions"],
            "Final Payment": payment_breakdown["final_payment"]
        }
        
        paysheet_data.append(row)
    
    return pd.DataFrame(paysheet_data)

def paysheet_generator_widget():
    """Streamlit widget for paysheet generation."""
    st.subheader("💰 Paysheet Generator")
    
    # Display current payment rules
    with st.expander("📋 Current Payment Rules"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Base Rate: {PAYMENT_RULES['base_rate']*100}%")
            st.write(f"Bonus Threshold: {PAYMENT_RULES['bonus_threshold']:,} diamonds")
        with col2:
            st.write(f"Bonus Rate: {PAYMENT_RULES['bonus_rate']*100}%")
            st.write(f"PK Win Bonus: {PAYMENT_RULES['pk_win_bonus']:,} diamonds")
            st.write(f"Attendance Bonus: {PAYMENT_RULES['attendance_bonus']:,} diamonds")
    
    # Manual host data entry
    st.subheader("📝 Add Host Data")
    
    with st.form("host_data_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            host_id = st.text_input("Host ID")
            host_name = st.text_input("Host Name")
        
        with col2:
            diamonds_earned = st.number_input("Diamonds Earned", min_value=0, value=0)
            days_worked = st.number_input("Days Worked", min_value=0, max_value=31, value=0)
        
        with col3:
            pk_wins = st.number_input("PK Wins", min_value=0, value=0)
            additional_bonuses = st.number_input("Additional Bonuses", min_value=0, value=0)
            deductions = st.number_input("Deductions", min_value=0, value=0)
        
        submit = st.form_submit_button("Add Host")
        
        if submit and host_id and host_name:
            # Initialize session state for hosts data
            if "hosts_data" not in st.session_state:
                st.session_state.hosts_data = []
            
            # Add new host data
            new_host = {
                "id": host_id,
                "name": host_name,
                "diamonds_earned": diamonds_earned,
                "days_worked": days_worked,
                "pk_wins": pk_wins,
                "additional_bonuses": additional_bonuses,
                "deductions": deductions
            }
            
            st.session_state.hosts_data.append(new_host)
            st.success(f"Added {host_name} to paysheet!")
    
    # Display current hosts and generate paysheet
    if "hosts_data" in st.session_state and st.session_state.hosts_data:
        st.subheader("👥 Current Hosts")
        
        # Generate and display paysheet
        paysheet_df = generate_paysheet(st.session_state.hosts_data)
        st.dataframe(paysheet_df, use_container_width=True)
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Hosts", len(paysheet_df))
        with col2:
            st.metric("Total Payout", f"${paysheet_df['Final Payment'].sum():.2f}")
        with col3:
            st.metric("Avg per Host", f"${paysheet_df['Final Payment'].mean():.2f}")
        
        # Download button
        csv = paysheet_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Paysheet CSV",
            data=csv,
            file_name=f"paysheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        # Clear data button
        if st.button("🗑️ Clear All Data"):
            st.session_state.hosts_data = []
            st.rerun()

def individual_payment_calculator():
    """Individual payment calculator widget."""
    st.subheader("🧮 Individual Payment Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        diamonds = st.number_input("Diamonds Earned", min_value=0, value=5000)
        pk_wins = st.number_input("PK Wins", min_value=0, value=3)
        days_worked = st.number_input("Days Worked", min_value=0, max_value=31, value=25)
    
    with col2:
        additional_bonuses = st.number_input("Additional Bonuses", min_value=0, value=0)
        deductions = st.number_input("Deductions", min_value=0, value=0)
    
    if st.button("Calculate Payment"):
        host = HostPayment("temp", "temp")
        host.diamonds_earned = diamonds
        host.pk_wins = pk_wins
        host.days_worked = days_worked
        host.additional_bonuses = additional_bonuses
        host.deductions = deductions
        
        breakdown = host.calculate_total_payment()
        
        st.success("💰 **Payment Breakdown:**")
        st.write(f"Base Payment: ${breakdown['base_payment']:.2f}")
        st.write(f"Performance Bonus: ${breakdown['performance_bonus']:.2f}")
        st.write(f"PK Bonus: ${breakdown['pk_bonus']:.2f}")
        st.write(f"Attendance Bonus: ${breakdown['attendance_bonus']:.2f}")
        st.write(f"Additional Bonuses: ${breakdown['additional_bonuses']:.2f}")
        st.write("---")
        st.write(f"**Total Before Deductions: ${breakdown['total_before_deductions']:.2f}**")
        st.write(f"Deductions: -${breakdown['deductions']:.2f}")
        st.write(f"**Final Payment: ${breakdown['final_payment']:.2f}**")
