#!/usr/bin/env python3
"""
CMS Shared Care Reduction Calculator (UK)
Based on Child Maintenance Service rules.
"""

def get_reduction_fraction(nights: int) -> tuple[float, str]:
    """Return the reduction fraction and label based on overnight stays."""
    if nights < 52:
        return 0, "No reduction (fewer than 52 nights)"
    elif 52 <= nights <= 103:
        return 1/7, "1/7 reduction (52–103 nights)"
    elif 104 <= nights <= 155:
        return 2/7, "2/7 reduction (104–155 nights)"
    elif 156 <= nights <= 174:
        return 3/7, "3/7 reduction (156–174 nights)"
    elif nights >= 175:
        # At 175+ nights (shared care roughly 50/50), support is halved then
        # an additional £7/wk is subtracted per child (CMS rules)
        return 1/2, "1/2 reduction (175+ nights — equal shared care)"
    return 0, "Unknown"


def calculate_reduction(base_amount: float, nights: int, num_children: int = 1) -> None:
    """Calculate and print the shared care reduction."""
    fraction, label = get_reduction_fraction(nights)

    reduction = base_amount * fraction
    reduced_amount = base_amount - reduction

    # At 175+ nights CMS also subtracts £7 per child per week
    extra_deduction = 0
    if nights >= 175:
        extra_deduction = 7 * num_children
        reduced_amount = max(0, reduced_amount - extra_deduction)

    print("\n" + "=" * 50)
    print("       CMS SHARED CARE REDUCTION RESULT")
    print("=" * 50)
    print(f"  Overnight stays per year : {nights} nights")
    print(f"  Reduction rule applied   : {label}")
    print(f"  Number of children       : {num_children}")
    print(f"  Base weekly maintenance  : £{base_amount:.2f}")
    print(f"  Reduction amount         : £{reduction:.2f}")
    if extra_deduction:
        print(f"  Additional £7 deduction  : £{extra_deduction:.2f} (£7 x {num_children} child(ren))")
    print(f"  Reduced weekly payment   : £{reduced_amount:.2f}")
    print("=" * 50 + "\n")


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("  Please enter a positive number.")
            else:
                return value
        except ValueError:
            print("  Invalid input — please enter a number (e.g. 125.50).")


def get_positive_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("  Please enter a positive whole number.")
            else:
                return value
        except ValueError:
            print("  Invalid input — please enter a whole number.")


def main():
    print("\n" + "=" * 50)
    print("    CMS SHARED CARE REDUCTION CALCULATOR (UK)")
    print("=" * 50)
    print("  Calculates the reduction in child maintenance")
    print("  when the paying parent shares overnight care.\n")

    while True:
        base_amount = get_positive_float("  Enter base weekly maintenance amount (£): ")
        nights = get_positive_int("  Enter number of overnight stays per year  : ")

        if nights > 365:
            print("  ⚠  Nights cannot exceed 365. Please re-enter.\n")
            continue

        num_children = get_positive_int("  Enter number of qualifying children       : ")

        calculate_reduction(base_amount, nights, num_children)

        again = input("  Calculate another? (y/n): ").strip().lower()
        if again != 'y':
            print("\n  Goodbye.\n")
            break
        print()


if __name__ == "__main__":
    main()