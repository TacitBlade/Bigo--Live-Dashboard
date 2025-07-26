def calculate_diamonds_breakdown(beans: int) -> tuple[int, int, list[dict[str, int]]]:
    """
    Converts beans to diamonds based on a tiered exchange system
    and returns a detailed breakdown of the exchanges.
    """
    diamonds: int = 0
    exchanges: list[tuple[int, int]] = [
        (10999, 3045),  # beans, diamonds
        (3999, 1105),
        (999, 275),
        (109, 29),
        (8, 2)
    ]

    remaining_beans: int = beans
    breakdown: list[dict[str, int]] = []

    for cost_beans, gained_diamonds in exchanges:
        if remaining_beans >= cost_beans:
            num_bundles: int = remaining_beans // cost_beans
            diamonds_from_bundle: int = num_bundles * gained_diamonds
            diamonds += diamonds_from_bundle
            remaining_beans -= num_bundles * cost_beans
            
            breakdown.append({
                "number_of_bundles": num_bundles,
                "bundle_cost_beans": cost_beans,
                "bundle_gained_diamonds": gained_diamonds,
                "diamonds_from_bundle": diamonds_from_bundle
            })

    return diamonds, remaining_beans, breakdown

def calculate_diamonds(beans: int) -> tuple[int, int]:
    """Converts beans to diamonds based on a tiered exchange system."""
    diamonds, remaining_beans, _ = calculate_diamonds_breakdown(beans)
    return diamonds, remaining_beans

if __name__ == "__main__":
    # Example usage:
    input_beans: int = int(input("Enter the number of beans: "))
    total_diamonds, remaining_beans, breakdown_details = calculate_diamonds_breakdown(input_beans)
    print(f"With {input_beans} beans, you would get {total_diamonds} diamonds. You would have {remaining_beans} beans remaining.")
    if breakdown_details:
        print("\nExchange Breakdown:")
        for item in breakdown_details:
            print(
                f"- {item['number_of_bundles']}x bundle(s) of {item['bundle_cost_beans']} beans "
                f"for {item['bundle_gained_diamonds']} diamonds each. "
                f"(Total from this bundle: {item['diamonds_from_bundle']} diamonds)"
            )
