#!/usr/bin/env python3
"""
SQE1 Litigation Costs Calculator (England & Wales)
Calculates judgment debt interest and proportionality assessment.
Explains each step as it runs.
"""

def divider():
    print("\n" + "=" * 60)

def section(title):
    print("\n" + "-" * 60)
    print(f"  {title}")
    print("-" * 60)

def explain(text):
    print(f"\n  >>> {text}")

def get_positive_float(prompt):
    while True:
        try:
            value = float(input(f"  {prompt}"))
            if value < 0:
                print("  Please enter a positive number.")
            else:
                return value
        except ValueError:
            print("  Invalid input — please enter a number (e.g. 5000.00).")

def get_positive_int(prompt):
    while True:
        try:
            value = int(input(f"  {prompt}"))
            if value <= 0:
                print("  Please enter a whole number greater than zero.")
            else:
                return value
        except ValueError:
            print("  Invalid input — please enter a whole number (e.g. 90).")

def calculate_judgment_interest(principal, days):
    """
    Calculates statutory interest on a judgment debt.
    Under the Judgments Act 1838, interest accrues at 8% per annum
    on the outstanding judgment debt from the date of judgment.
    """
    section("STEP 1 — JUDGMENT DEBT INTEREST")

    explain(
        "Under the Judgments Act 1838, once a court gives judgment, "
        "the losing party must pay statutory interest on the outstanding "
        "debt at a fixed rate of 8% per annum. This accrues daily until "
        "the debt is paid in full."
    )

    rate = 0.08
    interest = principal * rate * (days / 365)
    total_owed = principal + interest

    print(f"\n  Formula : Interest = Principal × 8% × (Days ÷ 365)")
    print(f"  Formula : Interest = £{principal:,.2f} × 0.08 × ({days} ÷ 365)")
    print(f"\n  Principal (judgment debt)  : £{principal:,.2f}")
    print(f"  Statutory interest rate    : 8% per annum (fixed by statute)")
    print(f"  Days since judgment        : {days} days")
    print(f"  Interest accrued           : £{interest:,.2f}")
    print(f"  Total now owed             : £{total_owed:,.2f}")

    explain(
        f"The winning party is owed £{principal:,.2f} in principal. "
        f"After {days} days at 8% per annum, interest of £{interest:,.2f} "
        f"has accrued, bringing the total to £{total_owed:,.2f}. "
        "This incentivises prompt payment by the losing party."
    )

    return interest, total_owed

def assess_proportionality(claim_value, costs_claimed):
    """
    Assesses whether costs are proportionate to the value of the claim.
    Under CPR 44.3(5), costs must be proportionate to the matter.
    The court will not allow disproportionate costs even if reasonably incurred.
    """
    section("STEP 2 — PROPORTIONALITY OF COSTS (CPR 44.3)")

    explain(
        "Under Civil Procedure Rules (CPR) 44.3(5), the court will only "
        "allow costs that are PROPORTIONATE to the value and complexity of "
        "the claim. Even if costs were reasonably incurred, they may be "
        "reduced if they are disproportionate. This is a key SQE1 concept."
    )

    ratio = (costs_claimed / claim_value) * 100

    print(f"\n  Formula : Costs Ratio = (Costs Claimed ÷ Claim Value) × 100")
    print(f"  Formula : Costs Ratio = (£{costs_claimed:,.2f} ÷ £{claim_value:,.2f}) × 100")
    print(f"\n  Claim value                : £{claim_value:,.2f}")
    print(f"  Costs claimed              : £{costs_claimed:,.2f}")
    print(f"  Costs as % of claim        : {ratio:.1f}%")

    # Proportionality banding — based on general CPR guidance
    if ratio <= 25:
        verdict = "LIKELY PROPORTIONATE"
        colour = "✔"
        detail = (
            "Costs are below 25% of the claim value. Courts generally "
            "regard this as proportionate and are unlikely to reduce them "
            "on proportionality grounds alone."
        )
    elif ratio <= 50:
        verdict = "BORDERLINE — MAY BE QUERIED"
        colour = "⚠"
        detail = (
            "Costs are between 25% and 50% of the claim value. A costs "
            "judge may query these and require justification, particularly "
            "for straightforward matters. Context and complexity matter."
        )
    elif ratio <= 100:
        verdict = "LIKELY DISPROPORTIONATE"
        colour = "✘"
        detail = (
            "Costs exceed 50% of the claim value. Courts are likely to "
            "find these disproportionate under CPR 44.3(5). They may be "
            "reduced on detailed assessment even if reasonably incurred."
        )
    else:
        verdict = "ALMOST CERTAINLY DISPROPORTIONATE"
        colour = "✘✘"
        detail = (
            "Costs exceed the value of the claim itself. This is a strong "
            "indicator of disproportionality. The court will almost certainly "
            "reduce costs on detailed assessment. Consider whether litigation "
            "was the appropriate course of action."
        )

    print(f"\n  Proportionality assessment : {colour}  {verdict}")
    explain(detail)

    return ratio, verdict

def calculate_fixed_costs(claim_value):
    """
    Fast track and small claims fixed cost guidance.
    Under CPR Part 45, fixed costs apply to certain track cases.
    """
    section("STEP 3 — TRACK ALLOCATION & FIXED COST GUIDANCE (CPR Part 26)")

    explain(
        "Civil claims are allocated to a 'track' based on value and complexity. "
        "The track determines how costs are assessed. Small claims (under £10,000) "
        "have very limited cost recovery. Fast track (£10,000–£25,000) uses fixed "
        "trial costs. Multi-track (over £25,000) allows full costs assessment."
    )

    if claim_value <= 10000:
        track = "SMALL CLAIMS TRACK"
        detail = (
            "Claims up to £10,000 are usually allocated to the small claims "
            "track. Cost recovery is very limited — generally only court fees "
            "and limited fixed sums. Legal costs are rarely recoverable. "
            "This discourages use of lawyers for low-value disputes."
        )
        recoverable = "Court fees + limited fixed costs only"
    elif claim_value <= 25000:
        track = "FAST TRACK"
        detail = (
            "Claims between £10,000 and £25,000 go to the fast track. "
            "Fixed trial costs apply under CPR Part 45. These are set figures "
            "regardless of time spent. The winning party recovers fixed costs, "
            "not actual costs."
        )
        recoverable = "Fixed trial costs under CPR Part 45"
    else:
        track = "MULTI-TRACK"
        detail = (
            "Claims over £25,000 are allocated to the multi-track. "
            "Costs are assessed on the standard or indemnity basis at a "
            "detailed assessment hearing. The court has full discretion. "
            "Costs budgeting (Precedent H) is usually required."
        )
        recoverable = "Assessed costs (standard or indemnity basis)"

    print(f"\n  Claim value                : £{claim_value:,.2f}")
    print(f"  Likely track               : {track}")
    print(f"  Recoverable costs          : {recoverable}")
    explain(detail)

def costs_summary(principal, days, interest, total_owed, costs_claimed, ratio, verdict):
    section("FINAL SUMMARY")

    explain(
        "Here is a complete summary of the litigation costs position. "
        "In an SQE1 question, you would be expected to identify the correct "
        "figure for interest, assess proportionality, and advise on track."
    )

    print(f"""
  ┌─────────────────────────────────────────────────────┐
  │              LITIGATION COSTS SUMMARY               │
  ├─────────────────────────────────────────────────────┤
  │  Judgment debt (principal)    : £{principal:>12,.2f}        │
  │  Days since judgment          : {days:>8} days            │
  │  Statutory interest (8% p.a.) : £{interest:>12,.2f}        │
  │  Total now owed               : £{total_owed:>12,.2f}        │
  ├─────────────────────────────────────────────────────┤
  │  Costs claimed                : £{costs_claimed:>12,.2f}        │
  │  Costs as % of claim          : {ratio:>11.1f}%        │
  │  Proportionality verdict      : {verdict:<23}  │
  └─────────────────────────────────────────────────────┘
""")

    explain(
        "KEY SQE1 RULES TO REMEMBER: "
        "(1) Judgment interest = 8% p.a. under the Judgments Act 1838. "
        "(2) Costs must be proportionate under CPR 44.3(5). "
        "(3) Track allocation determines cost recovery rules. "
        "(4) 'Costs follow the event' — loser usually pays winner's costs (CPR 44.2)."
    )

def main():
    divider()
    print("      SQE1 LITIGATION COSTS CALCULATOR (England & Wales)")
    print("      Based on CPR, Judgments Act 1838 & SQE1 FLK1 syllabus")
    divider()

    explain(
        "This tool walks through the key litigation costs calculations "
        "tested in SQE1 FLK1. It covers: (1) statutory interest on judgment "
        "debts, (2) proportionality of costs under CPR 44.3(5), and "
        "(3) track allocation under CPR Part 26."
    )

    while True:
        print("\n  Please enter the details of the case:\n")

        principal     = get_positive_float("Judgment debt amount (£): ")
        days          = get_positive_int("Days since judgment was entered: ")
        costs_claimed = get_positive_float("Total costs claimed by winning party (£): ")

        interest, total_owed = calculate_judgment_interest(principal, days)
        ratio, verdict       = assess_proportionality(principal, costs_claimed)
        calculate_fixed_costs(principal)
        costs_summary(principal, days, interest, total_owed,
                      costs_claimed, ratio, verdict)

        again = input("\n  Run another calculation? (y/n): ").strip().lower()
        if again != 'y':
            print("\n  Good luck with your SQE1 revision.\n")
            break

if __name__ == "__main__":
    main()