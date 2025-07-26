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
            
        # Read Excel with header row - try different header positions
        rules_df = pd.read_excel(excel_path, sheet_name=sheet_to_use, header=0)
        
        # Debug: Show raw data structure
        st.write("**Debug - Raw Excel Data:**")
        st.dataframe(rules_df.head())
        
        # Check if we need to use a different header row
        if all(col.startswith('Unnamed:') for col in rules_df.columns):
            # Try reading with header=1 (second row as header)
            rules_df = pd.read_excel(excel_path, sheet_name=sheet_to_use, header=1)
            st.write("**Debug - Using row 2 as header:**")
            st.dataframe(rules_df.head())
            
            # If still unnamed, try header=2
            if all(col.startswith('Unnamed:') for col in rules_df.columns):
                rules_df = pd.read_excel(excel_path, sheet_name=sheet_to_use, header=2)
                st.write("**Debug - Using row 3 as header:**")
                st.dataframe(rules_df.head())
        
        # If columns are still unnamed, manually assign column names based on your image
        if all(col.startswith('Unnamed:') for col in rules_df.columns):
            # Based on your image, the columns should be:
            # Win, win, PK points, Star Tasks PK, Agency 2 vs 2 PK, Talent PK, Daily PK
            expected_columns = ['Win', 'win', 'PK points', 'Star Tasks PK', 'Agency 2 vs 2 PK', 'Talent PK', 'Daily PK']
            
            # Only assign if we have enough columns
            if len(rules_df.columns) >= len(expected_columns):
                rules_df.columns = expected_columns[:len(rules_df.columns)]
            else:
                # Generic column names if we don't have enough
                rules_df.columns = [f'Column_{i+1}' for i in range(len(rules_df.columns))]
            
            st.write("**Debug - After assigning column names:**")
            st.dataframe(rules_df.head())
        
        # Now process the data to create PK Type and Diamond Requirement columns
        pk_data = []
        
        # Define PK types from your columns
        pk_columns = ['Daily PK', 'Talent PK', 'Agency 2 vs 2 PK', 'Star Tasks PK']
        
        # Process each row
        for idx, row in rules_df.iterrows():
            # Get win amount from 'Win' or 'win' column
            win_amount = "N/A"
            if 'Win' in rules_df.columns and pd.notna(row['Win']):
                win_amount = row['Win']
            elif 'win' in rules_df.columns and pd.notna(row['win']):
                win_amount = row['win']
            
            # Process each PK type column
            for pk_type in pk_columns:
                if pk_type in rules_df.columns and pd.notna(row[pk_type]):
                    pk_score_raw = str(row[pk_type]).strip()
                    
                    # Extract numeric value from PK score (remove ')' or other characters)
                    try:
                        pk_score = int(pk_score_raw.rstrip(')').replace(',', ''))
                        diamond_req = pk_score // 10  # Convert PK score to diamond requirement
                        
                        if diamond_req > 0:
                            pk_data.append({
                                'PK Type': pk_type,
                                'PK Score': pk_score,
                                'Diamond Requirement': diamond_req,
                                'Win': win_amount
                            })
                    except (ValueError, AttributeError):
                        continue
        
        if not pk_data:
            st.error("No valid PK data could be extracted from the Excel file.")
            st.write("**Available columns:**", list(rules_df.columns))
            return None
        
        # Convert to DataFrame
        processed_df = pd.DataFrame(pk_data)
        
        # Remove duplicates and sort
        processed_df = processed_df.drop_duplicates().sort_values('Diamond Requirement', ascending=False)
        
        st.success(f"Successfully processed {len(processed_df)} PK types!")
        st.write("**Final processed data:**")
        st.dataframe(processed_df)
        
        return processed_df
        
    except FileNotFoundError:
        st.error("Error: 'RulesAndRewards.xlsx' not found. Please make sure the file is in the 'templates' directory.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the rules: {e}")
        st.write("**Error details:**", str(e))
        return None

def calculate_pk_breakdown(diamonds: int, rules_df: pd.DataFrame) -> str:
    """Calculates the optimal PK breakdown based on diamond input."""
    
    # Check for required columns
    required_columns = ['PK Type', 'Diamond Requirement']
    missing_columns = [col for col in required_columns if col not in rules_df.columns]
    
    if missing_columns:
        available_columns = list(rules_df.columns)
        return f"Missing required columns: {missing_columns}. Available columns: {available_columns}"

    # Create a copy and clean the data
    rules_copy = rules_df.copy()
    rules_copy = rules_copy.dropna(subset=['Diamond Requirement', 'PK Type'])
    
    # Ensure Diamond Requirement is numeric and sort by descending value
    rules_copy['Diamond Requirement'] = pd.to_numeric(rules_copy['Diamond Requirement'], errors='coerce')
    rules_copy = rules_copy.dropna(subset=['Diamond Requirement'])
    rules_copy = rules_copy.sort_values(by='Diamond Requirement', ascending=False)

    remaining_diamonds = diamonds
    breakdown = []

    for _, row in rules_copy.iterrows():
        diamond_req = int(row['Diamond Requirement'])
        pk_type = str(row['PK Type'])
        pk_score = int(row['PK Score']) if 'PK Score' in row and pd.notna(row['PK Score']) else diamond_req * 10
        win_amount = row['Win'] if 'Win' in row and pd.notna(row['Win']) else "N/A"
        
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
