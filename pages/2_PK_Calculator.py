import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="💎 PK Calculator", layout="wide")

def load_rules():
    """Loads PK rules from the Excel file."""
    try:
        # Correctly construct the path to the Excel file
        excel_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'RulesAndRewards.xlsx')
        
        # Try to read the Excel file and get available sheet names
        excel_file = pd.ExcelFile(excel_path)
        sheet_names = excel_file.sheet_names
        
        # Try common sheet names or use the first available sheet
        sheet_to_use = None
        common_names = ['Sheet1', 'Rules', 'PK Rules', 'Data']
        
        for name in common_names:
            if name in sheet_names:
                sheet_to_use = name
                break
        
        # If no common name found, use the first sheet
        if sheet_to_use is None and sheet_names:
            sheet_to_use = sheet_names[0]
            st.info(f"Using sheet '{sheet_to_use}' from the Excel file.")
        
        if sheet_to_use is None:
            st.error("No sheets found in the Excel file.")
            return None
            
        rules_df = pd.read_excel(excel_path, sheet_name=sheet_to_use)
        
        # Debug: Show available columns
        st.info(f"Available columns: {list(rules_df.columns)}")
        
        # Debug: Show first few rows
        st.info("First few rows of data:")
        st.dataframe(rules_df.head())
        
        # Process the diamond requirements from PK Score (divide by 10)
        if 'PK Score' in rules_df.columns:
            # Convert PK Score to diamond requirement by dividing by 10 (removing a zero)
            rules_df['Diamond Requirement'] = pd.to_numeric(rules_df['PK Score'], errors='coerce') / 10
        
        return rules_df
    except FileNotFoundError:
        st.error("Error: 'RulesAndRewards.xlsx' not found. Please make sure the file is in the 'templates' directory.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the rules: {e}")
        return None

def calculate_pk_breakdown(diamonds: int, rules_df: pd.DataFrame) -> str:
    """Calculates the optimal PK breakdown based on diamond input."""
    
    # Check for required columns
    if 'PK Type' not in rules_df.columns or 'Diamond Requirement' not in rules_df.columns:
        available_columns = list(rules_df.columns)
        return f"Missing required columns. Available columns: {available_columns}. Need 'PK Type' and 'Diamond Requirement' (calculated from PK Score)."

    # Create a copy and clean the data
    rules_copy = rules_df.copy()
    rules_copy = rules_copy.dropna(subset=['Diamond Requirement', 'PK Type'])
    rules_copy = rules_copy.sort_values(by='Diamond Requirement', ascending=False)

    remaining_diamonds = diamonds
    breakdown = []

    for _, row in rules_copy.iterrows():
        diamond_req = int(row['Diamond Requirement'])
        pk_type = row['PK Type']
        pk_score = int(row['PK Score']) if 'PK Score' in row else diamond_req * 10
        win_amount = row['Win'] if 'Win' in row else "N/A"
        
        if remaining_diamonds >= diamond_req:
            num_pks = int(remaining_diamonds // diamond_req)
            breakdown.append(f"- **{pk_type}** (PK Score: {pk_score:,}): {num_pks} time(s) ({num_pks * diamond_req:,} diamonds) - Win: {win_amount}")
            remaining_diamonds %= diamond_req

    if not breakdown:
        return "You do not have enough diamonds for any PK events."

    # Add remaining diamonds info
    result = "\n".join(breakdown)
    if remaining_diamonds > 0:
        result += f"\n\n**Remaining diamonds**: {remaining_diamonds:,}"
    
    return result

# --- Streamlit App ---
st.title("💎 PK Rewards Calculator")
st.info("Enter the amount of diamonds you have to see a breakdown of PK types for maximum win gains.")

# Load rules with caching for better performance
@st.cache_data
def get_cached_rules():
    return load_rules()

rules = get_cached_rules()

if rules is not None:
    # Display available PK types for reference
    with st.expander("📋 Available PK Types", expanded=False):
        if 'PK Type' in rules.columns and 'Diamond Requirement' in rules.columns:
            display_rules = rules[['PK Type', 'Diamond Requirement']].copy()
            display_rules = display_rules.dropna().sort_values('Diamond Requirement')
            st.dataframe(display_rules, use_container_width=True, hide_index=True)
    
    # Create input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        diamonds = st.number_input(
            "💎 Enter your diamonds", 
            min_value=0, 
            step=100, 
            value=0,
            help="Enter the total number of diamonds you have available"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        calculate_button = st.button("🧮 Calculate", type="primary", use_container_width=True)

    if calculate_button or diamonds > 0:
        if diamonds > 0:
            st.subheader("🎯 Recommended PK Strategy")
            breakdown_text = calculate_pk_breakdown(diamonds, rules)
            st.markdown(breakdown_text)
            st.success("✅ Calculation complete!")
        else:
            st.warning("⚠️ Please enter a diamond amount greater than 0.")
else:
    st.error("❌ PK calculation is currently unavailable as the rules could not be loaded.")
    st.info("💡 Please ensure the 'RulesAndRewards.xlsx' file exists in the templates directory.")
