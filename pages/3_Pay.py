import streamlit as st
from utils.calculators import pk_calculator_widget, target_calculator_widget, conversion_calculator_widget
from utils.paysheet import paysheet_generator_widget, individual_payment_calculator

st.set_page_config(page_title="💸 Pay Sheet", layout="wide")
st.title("💸 Host Pay Sheet & Calculators")

st.info("💰 Comprehensive payment calculations and host performance tools.")

# Main tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["💰 Paysheet Generator", "🧮 Calculators", "🎯 Targets", "🔄 Conversions"])

with tab1:
    st.header("💰 Paysheet Generation")
    paysheet_generator_widget()
    
    st.markdown("---")
    st.subheader("🧮 Individual Calculator")
    individual_payment_calculator()

with tab2:
    st.header("🧮 Performance Calculators")
    pk_calculator_widget()

with tab3:
    st.header("🎯 Target Analysis")
    target_calculator_widget()

with tab4:
    st.header("🔄 Conversion Tools")
    conversion_calculator_widget()

# Footer with tips
st.markdown("---")
st.markdown("""
### � Payment Tips:
- **Base Rate**: 40% of diamonds earned
- **Performance Bonus**: Additional 10% for diamonds > 10K
- **PK Win Bonus**: 500 diamonds per PK victory
- **Attendance Bonus**: 1000 diamonds for perfect attendance (30 days)
- Review payment rules regularly with management
""")
