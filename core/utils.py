def validate_inputs(buy_price, sell_price, quantity, exchange):
    if buy_price <= 0 or sell_price <= 0:
        raise ValueError("Buy and Sell prices must be greater than 0.")
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
    if exchange.upper() not in ["NSE", "BSE"]:
        raise ValueError("Exchange must be 'NSE' or 'BSE'.")

def round2(value):
    """Round to 2 decimals safely."""
    return round(float(value), 2)
