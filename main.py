import math
import sys

# US Cents / Hour
RATE_STD = 0
RATE_OT = 0   

# Hours
OT_THRESHOLD = 40


# i/o Info
H_TO_W_MODE = "+"
W_TO_H_MODE = "-"
MODES = {
    H_TO_W_MODE,
    W_TO_H_MODE
}

BAD_USE_MSG = "wages: Bad usage\nExpected: wages (+|-) N, where N is a floating-point value"


def main():
    try:
        flag = sys.argv[1]
        n = float(sys.argv[2])
        assert flag in MODES
        assert n >= 0
    except:
        # If anything breaks, assume it's because of bad input.
        # Print out expected usage
        print(BAD_USE_MSG, file=sys.stderr)
        exit(1)
    if flag == H_TO_W_MODE:
        print(f"${hours_to_paycheck(n):.2f} earned after {n:.1f} hours")
    elif flag == W_TO_H_MODE:
        h = paycheck_to_hours(n)
        print(f"{h:.1f} hours needed for >= ${n:.2f} (${hours_to_paycheck(h):.2f})")


def hours_to_paycheck(hours):
    g = gross(hours)
    w = withholdings(g)
    return (g - w) / 100


def paycheck_to_hours(target):
    h = 0
    wages = hours_to_paycheck(h)
    while wages - target < 0:
        h += 0.2
        wages = hours_to_paycheck(h)
    return h


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


if __name__ == "__main__":
    main()
