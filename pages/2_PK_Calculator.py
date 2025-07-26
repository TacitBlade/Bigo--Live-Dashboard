# streamlit_app.py

import streamlit as st

# PK tier definitions with corrected data types and formatting
PK_TIERS = {
    "Daily PK": [(100000, 1800), (50000, 1000), (30000, 900), (20000, 600), (10000, 300), (7000, 210)],
    "Talent PK": [(50000, 1700), (30000, 1000), (20000, 700), (10000, 350), (5000, 150)],
    "2 vs 2 PK": [(100000, 3500), (70000, 2300), (50000, 1700), (25000, 800), (10000, 300), (5000, 150)],
    "Star Tasks PK": [(120000, 4000), (100000, 3500), (80000, 2800), (50000, 1700), (10000, 320), (2000, 60)],
    "Agency PK Party": [(150000, "25%")],  # Fixed percentage formatting
    "Agency Glory PK": [(900000, 35000), (300000, 12000), (100000, 4000), (70000, 2800), (50000, 2000), (30000, 1200)]
}

def diamonds_to_score(diamonds: int) -> int:
    """Convert diamonds to PK score using 1:10 ratio"""
    return diamonds * 10

def format_number(num):
    """Format numbers with comma separators"""
    if isinstance(num, (int, float)):
        return f"{num:,}"
    return str(num)

def calculate_rebates(score: int):
    """Calculate rebates for all PK types based on score"""
    result = []
    for pk_type, tiers in PK_TIERS.items():
        tier_found = False
        for threshold, rebate in sorted(tiers, reverse=True):
            if score >= threshold:
                result.append((pk_type, threshold, rebate, True))
                tier_found = True
                break
        if not tier_found:
            # Show the lowest tier requirement
            lowest_threshold = min(tiers, key=lambda x: x[0])[0]
            result.append((pk_type, lowest_threshold, "Not eligible", False))
    
    return result

def display_results(breakdown):
    """Display results with improved formatting and color coding"""
    eligible_count = 0
    
    st.markdown("### 📊 Rebate Breakdown")
    
    for pk_type, threshold, rebate, is_eligible in breakdown:
        if is_eligible:
            eligible_count += 1
            st.success(f"✅ **{pk_type}**")
            st.write(f"• **PK Score Required:** {format_number(threshold)}")
            st.write(f"• **Rebate:** {format_number(rebate)} diamonds")
        else:
            st.error(f"❌ **{pk_type}**")
            st.write(f"• **Minimum Required:** {format_number(threshold)}")
            st.write(f"• **Status:** {rebate}")
        st.write("---")
    
    # Summary
    st.markdown(f"### 📈 Summary")
    st.info(f"You're eligible for **{eligible_count}** out of **{len(breakdown)}** PK types")

def calculate_best_investment(current_diamonds: int):
    """Calculate the best investment to reach next tier"""
    current_score = diamonds_to_score(current_diamonds)
    suggestions = []
    
    for pk_type, tiers in PK_TIERS.items():
        for threshold, rebate in sorted(tiers):
            if current_score < threshold:
                diamonds_needed = (threshold - current_score) // 10
                roi = rebate if isinstance(rebate, (int, float)) else 0
                if roi > 0:
                    efficiency = roi / diamonds_needed if diamonds_needed > 0 else 0
                    suggestions.append((pk_type, diamonds_needed, roi, efficiency))
                break
    
    return sorted(suggestions, key=lambda x: x[3], reverse=True)[:3]

# ----- Streamlit UI -----
st.set_page_config(
    page_title="PK Rebate Calculator", 
    page_icon="💎", 
    layout="centered"
)

st.title("💎 PK Rebate Optimizer")
st.markdown("Calculate your PK rebates and find the best investment opportunities!")

# Input section
col1, col2 = st.columns(2)
with col1:
    diamonds = st.number_input(
        "💎 Enter diamond amount", 
        min_value=0, 
        step=100,
        help="Enter the number of diamonds you plan to spend"
    )

with col2:
    st.metric(
        "PK Score", 
        format_number(diamonds_to_score(diamonds)) if diamonds > 0 else "0"
    )

# Calculate button
if st.button("🚀 Calculate Rebates", type="primary"):
    if diamonds > 0:
        pk_score = diamonds_to_score(diamonds)
        
        # Main results
        breakdown = calculate_rebates(pk_score)
        display_results(breakdown)
        
        # Investment suggestions
        suggestions = calculate_best_investment(diamonds)
        if suggestions:
            st.markdown("### 💡 Investment Suggestions")
            st.markdown("*Best opportunities to reach the next tier:*")
            
            for i, (pk_type, diamonds_needed, roi, efficiency) in enumerate(suggestions, 1):
                with st.expander(f"{i}. {pk_type} - Need {format_number(diamonds_needed)} more diamonds"):
                    st.write(f"• **Investment:** {format_number(diamonds_needed)} diamonds")
                    st.write(f"• **Rebate:** {format_number(roi)} diamonds")
                    st.write(f"• **ROI:** {efficiency:.2%}")
    else:
        st.warning("Please enter a diamond amount greater than 0")

# Information section
with st.expander("ℹ️ How it works"):
    st.markdown("""
    **PK Score Calculation:** 1 diamond = 10 PK points
    
    **PK Types Available:**
    - Daily PK, Talent PK, 2 vs 2 PK
    - Star Tasks PK, Agency PK Party, Agency Glory PK
    
    **Tips:**
    - Focus on PK types where you're close to the next tier
    - Consider ROI when planning your diamond spending
    - Agency Glory PK offers the highest rebates but requires significant investment
    """)