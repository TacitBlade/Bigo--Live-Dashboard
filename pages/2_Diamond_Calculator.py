import streamlit as st
from utils.calculators import calculate_diamonds_breakdown

def show_diamond_calculator():
    """
    Streamlit page for calculating diamond exchanges from beans
    and showing a detailed breakdown.
    """
    st.set_page_config(page_title="Diamond Calculator", page_icon="💎", layout="wide")

    st.title("💎 Diamond Exchange Calculator")
    st.markdown("Enter the number of beans you have to see how many diamonds you can exchange for and a detailed breakdown of the transaction.")

    st.divider()

    beans_input = st.number_input(
        "Enter the number of beans", 
        min_value=0, 
        value=0, 
        step=1000,
        help="Enter the total amount of beans you want to convert."
    )

    if st.button("Calculate Diamonds", use_container_width=True):
        if beans_input > 0:
            total_diamonds, remaining_beans, breakdown = calculate_diamonds_breakdown(beans_input)

            st.success(f"**With {beans_input:,} beans, you can get a total of {total_diamonds:,} diamonds, with {remaining_beans:,} beans remaining.**")
            
            if breakdown:
                st.subheader("Exchange Breakdown:")
                for item in breakdown:
                    st.info(
                        f"**{item['number_of_bundles']}x** bundle(s) of **{item['bundle_cost_beans']:,} beans** "
                        f"for **{item['bundle_gained_diamonds']:,} diamonds** each. "
                        f"(Total from this bundle: **{item['diamonds_from_bundle']:,}** diamonds)"
                    )
            else:
                st.warning("No bundles could be purchased with the provided amount of beans.")
        else:
            st.warning("Please enter a number of beans greater than 0.")

if __name__ == "__main__":
    show_diamond_calculator()
