import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="� PK Calculator", layout="wide")

def load_rules():
    """Loads PK rules from the Excel file."""
    try:
        # Correctly construct the path to the Excel file
        excel_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'RulesAndRewards.xlsx')
        rules_df = pd.read_excel(excel_path, sheet_name='Sheet1')
        return rules_df
    except FileNotFoundError:
        st.error("Error: 'RulesAndRewards.xlsx' not found. Please make sure the file is in the 'templates' directory.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the rules: {e}")
        return None

def calculate_pk_breakdown(diamonds: int, rules_df: pd.DataFrame) -> str:
    """Calculates the optimal PK breakdown based on diamond input."""
    if 'Diamond Requirement' not in rules_df.columns or 'PK Type' not in rules_df.columns:
        return "Could not calculate breakdown due to missing or invalid rules data."

    # Ensure 'Diamond Requirement' is numeric and sort by it descending
    rules_df['Diamond Requirement'] = pd.to_numeric(rules_df['Diamond Requirement'], errors='coerce')
    rules_df.dropna(subset=['Diamond Requirement'], inplace=True)
    rules_df.sort_values(by='Diamond Requirement', ascending=False, inplace=True)

    remaining_diamonds = diamonds
    breakdown = []

    for _, row in rules_df.iterrows():
        diamond_req = row['Diamond Requirement']
        pk_type = row['PK Type']
        
        if remaining_diamonds >= diamond_req:
            num_pks = int(remaining_diamonds // diamond_req)
            breakdown.append(f"- **{pk_type}**: {num_pks} time(s)")
            remaining_diamonds %= diamond_req

    if not breakdown:
        return "You do not have enough diamonds for any PK events."

    return "\n".join(breakdown)

# --- Streamlit App ---
st.title("💎 PK Rewards Calculator")
st.info("Enter the amount of diamonds you have to see a breakdown of PK types for maximum win gains.")

rules = load_rules()

if rules is not None:
    diamonds = st.number_input("Enter your diamonds", min_value=0, step=100)

    if st.button("Calculate"):
        if diamonds > 0:
            st.subheader("Recommended PK Strategy")
            breakdown_text = calculate_pk_breakdown(diamonds, rules)
            st.markdown(breakdown_text)
        else:
            st.warning("Please enter a diamond amount.")
else:
    st.warning("PK calculation is currently unavailable as the rules could not be loaded.")
