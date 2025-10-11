from core.constants import (
    BROKERAGE_RATE, BROKERAGE_CAP,
    NSE_TXN_CHARGE, BSE_TXN_CHARGE,
    STT_RATE, SEBI_CHARGE_RATE,
    STAMP_DUTY_RATE, GST_RATE
)
from core.utils import validate_inputs, round2


def zerodha_intraday_pnl(buy_price: float, sell_price: float, quantity: int, exchange: str = "NSE") -> dict:
    """
    Pure function to calculate Zerodha Intraday Equity P&L.
    Returns all computed values in a dictionary.
    """

    # Validate inputs
    validate_inputs(buy_price, sell_price, quantity, exchange)

    # --- Basic Turnovers ---
    buy_turnover = buy_price * quantity
    sell_turnover = sell_price * quantity
    total_turnover = buy_turnover + sell_turnover

    # --- Brokerage ---
    brokerage_buy = min(BROKERAGE_CAP, BROKERAGE_RATE * buy_turnover)
    brokerage_sell = min(BROKERAGE_CAP, BROKERAGE_RATE * sell_turnover)
    brokerage = brokerage_buy + brokerage_sell

    # --- Exchange Txn Charges ---
    exchange_txn = (
        NSE_TXN_CHARGE * total_turnover
        if exchange.upper() == "NSE"
        else BSE_TXN_CHARGE * total_turnover
    )

    # --- Statutory Charges ---
    stt = STT_RATE * sell_turnover
    sebi = SEBI_CHARGE_RATE * total_turnover
    stamp_duty = STAMP_DUTY_RATE * buy_turnover
    gst = GST_RATE * (brokerage + exchange_txn + sebi)

    # --- Total ---
    zerodha_charges = brokerage
    statutory_charges = stt + exchange_txn + sebi + stamp_duty + gst
    total_charges = zerodha_charges + statutory_charges

    # --- P&L ---
    gross_pnl = (sell_price - buy_price) * quantity
    net_pnl = gross_pnl - total_charges
    points_to_breakeven = total_charges / quantity

    return {
        "Turnover": round2(total_turnover),
        "Zerodha Brokerage": round2(zerodha_charges),
        "Exchange Txn Charges": round2(exchange_txn),
        "SEBI Charges": round2(sebi),
        "Stamp Duty": round2(stamp_duty),
        "STT": round2(stt),
        "GST": round2(gst),
        "Total Charges": round2(total_charges),
        "Points to Breakeven": round2(points_to_breakeven),
        "Gross P&L": round2(gross_pnl),
        "Net P&L": round2(net_pnl)
    }
