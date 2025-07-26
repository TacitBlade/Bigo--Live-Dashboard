# streamlit_app.py

import streamlit as st

# PK tier definitions
PK_TIERS = {
    "Daily PK": [(100000, 1800), (50000, 1000), (30000, 900), (20000, 600), (10000, 300), (7000, 210)],
    "Talent PK": [(50000, 1700), (30000, 1000), (20000, 700), (10000, 350), (5000, 150)],
    "2 vs 2 PK": [(100000, 3500), (70000, 2300), (50000, 1700), (25000, 800), (10000, 300), (5000, 150)],
    "Star Tasks PK": [(120000, 4000), (100000, 3500), (80000, 2800), (50000, 1700), (10000, 320), (2000, 60)],
    "Agency PK Party": [(150000, 0.25)],
    "Agency Glory PK": [(900000, 35000), (300000, 12000), (100000, 4000), (70000, 2800), (50000, 2000), (30000, 1200)]
}

def diamonds_to_score(diamonds: int) -> int:
    return diamonds * 10

def calculate_rebates(score: int):
    result = []
    for pk_type, tiers in PK_TIERS.items():
        tier_found = False
        for threshold, rebate in sorted(tiers, reverse=True):
            if score >= threshold:
                result.append((pk_type, threshold, rebate))
                tier_found = True
                break
        if not tier_found:
            result.append((pk_type, "Below minimum", "No rebate available"))
    
    return result

def display_results(breakdown):
    for pk_type, threshold, rebate in breakdown:
        st.markdown(f"**{pk_type}**")
        st.write(f"• PK Threshold: {threshold}")
        st.write(f"• Rebate: {rebate}")
        st.write("---")

# ----- Streamlit UI -----
st.set_page_config(page_title="PK Rebate Calculator", layout="centered")
st.title("💎 PK Rebate Optimizer")
st.markdown("Enter your diamonds to get the best PK matchups for max rebates.")

diamonds = st.number_input("Enter diamond amount", min_value=1, step=1)

if st.button("Calculate"):
    pk_score = diamonds_to_score(diamonds)
    st.markdown(f"### Your PK Score: {pk_score}")
    breakdown = calculate_rebates(pk_score)
    display_results(breakdown)