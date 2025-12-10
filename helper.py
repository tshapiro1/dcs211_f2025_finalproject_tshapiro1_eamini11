
def fmt_num(x):
    """
    Format a number with comma separators.
    Example: 15230.55 -> '15,230.55'
    Returns 'N/A' if None.
    """
    if x is None:
        return "N/A"
    try:
        return f"{x:,}"
    except:
        return str(x)

def fmt_large(x):
    """
    Format large numbers into human-readable form.
    Example: 1,530,000,000 -> '1.53B'
    """
    if x is None:
        return "N/A"
    try:
        if x >= 1_000_000_000:
            return f"{x / 1_000_000_000:.2f}B"
        elif x >= 1_000_000:
            return f"{x / 1_000_000:.2f}M"
        elif x >= 1_000:
            return f"{x / 1_000:.2f}K"
        else:
            return str(x)
    except:
        return str(x)