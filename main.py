import math
import sys

# US Cents / Hour
RATE_STD = 1981  
RATE_OT = 2972   

# Hours
OT_THRESHOLD = 40


def main():
    try:
        h = float(sys.argv[1])
        g = gross(h)
        w = withholdings(g)
        print(as_usd(g - w))
    except (ValueError, IndexError):
        # If given none/invalid input, return -1 to signal failure
        print(-1)


# Return gross earnings (in cents) based on number of worked hours (as float)
def gross(hours):
    total = 0
    if hours > OT_THRESHOLD:
        total += RATE_OT * (hours - OT_THRESHOLD)
        hours = OT_THRESHOLD
    total += hours * RATE_STD
    return int(total)


# Return total tax withholdings (in cents) based on gross earnings (in cents)
def withholdings(gross):
    total = 0

    # Convert gross in cents to float $ amount for Quad. Regression
    n = float(gross) / 100  

    # Federal Tax Estimate (per Quad. Regression using Desmos)
    total += (0.0000526828*n*n) + (0.0449473*n) - 13.36
    # Colorado State Tax Estimate (rounded-down 4.5% of gross)
    total += math.floor(n * 0.045)
    # FICA Tax Estimate (6.2% of gross)
    total += n * 0.062
    # Medicare Tax Estimate (1.45% of gross)
    total += n * 0.0145
    # FAMLI Tax Estimate (0.45% of gross)
    total += n * 0.0045

    # Return deducted total as integer # of cents
    return 0 if total <= 0 else int(total * 100)


# Return the string representation of a number of cents as dollars
def as_usd(c):
    dollars, cents = divmod(int(c), 100)
    return f"${dollars}.{cents:02d}"


if __name__ == "__main__":
    main()
