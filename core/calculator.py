from core.constants import (
    BROKERAGE_RATE, BROKERAGE_CAP,
    NSE_TXN_CHARGE, BSE_TXN_CHARGE,
    STT_RATE, SEBI_CHARGE_RATE,
    STAMP_DUTY_RATE, GST_RATE
)
from core.utils import validate_inputs, round2


def zerodha_intraday_pnl1(buy_price: float, sell_price: float, quantity: int, exchange: str = "NSE") -> dict:
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

def calculate_turnover(buy_price: float, sell_price: float, quantity: int) -> dict:
    buy_turnover = buy_price * quantity
    sell_turnover = sell_price * quantity
    total_turnover = buy_turnover + sell_turnover
    return {
        "buy_turnover": buy_turnover,
        "sell_turnover": sell_turnover,
        "total_turnover": total_turnover
    }

def calculate_brokerage(buy_turnover: float, sell_turnover: float) -> float:
    brokerage_buy = min(BROKERAGE_CAP, BROKERAGE_RATE * buy_turnover)
    brokerage_sell = min(BROKERAGE_CAP, BROKERAGE_RATE * sell_turnover)
    return brokerage_buy + brokerage_sell

def calculate_exchange_txn(total_turnover: float, exchange: str) -> float:
    if exchange.upper() == "NSE":
        return NSE_TXN_CHARGE * total_turnover
    else:
        return BSE_TXN_CHARGE * total_turnover

def calculate_statutory_charges(buy_turnover: float, sell_turnover: float, total_turnover: float, brokerage: float, exchange_txn: float) -> dict:
    stt = STT_RATE * sell_turnover
    sebi = SEBI_CHARGE_RATE * total_turnover
    stamp_duty = STAMP_DUTY_RATE * buy_turnover
    gst = GST_RATE * (brokerage + exchange_txn + sebi)
    total_statutory = stt + sebi + stamp_duty + exchange_txn + gst
    return {
        "STT": stt,
        "SEBI": sebi,
        "Stamp Duty": stamp_duty,
        "GST": gst,
        "Total Statutory Charges": total_statutory
    }

def calculate_pnl(buy_price: float, sell_price: float, quantity: int, total_charges: float) -> dict:
    gross_pnl = (sell_price - buy_price) * quantity
    net_pnl = gross_pnl - total_charges
    points_to_breakeven = total_charges / quantity
    return {
        "Gross P&L": gross_pnl,
        "Net P&L": net_pnl,
        "Points to Breakeven": points_to_breakeven
    }

def zerodha_intraday_pnl(buy_price: float, sell_price: float, quantity: int, exchange: str = "NSE") -> dict:
    validate_inputs(buy_price, sell_price, quantity, exchange)

    turnovers = calculate_turnover(buy_price, sell_price, quantity)
    brokerage = calculate_brokerage(turnovers["buy_turnover"], turnovers["sell_turnover"])
    exchange_txn = calculate_exchange_txn(turnovers["total_turnover"], exchange)
    statutory_charges = calculate_statutory_charges(
        turnovers["buy_turnover"], turnovers["sell_turnover"], turnovers["total_turnover"], brokerage, exchange_txn
    )
    total_charges = brokerage + statutory_charges["Total Statutory Charges"]
    pnl = calculate_pnl(buy_price, sell_price, quantity, total_charges)

    return {
        "Turnover": round2(turnovers["total_turnover"]),
        "Zerodha Brokerage": round2(brokerage),
        "Exchange Txn Charges": round2(exchange_txn),
        "SEBI Charges": round2(statutory_charges["SEBI"]),
        "Stamp Duty": round2(statutory_charges["Stamp Duty"]),
        "STT": round2(statutory_charges["STT"]),
        "GST": round2(statutory_charges["GST"]),
        "Total Charges": round2(total_charges),
        "Points to Breakeven": round2(pnl["Points to Breakeven"]),
        "Gross P&L": round2(pnl["Gross P&L"]),
        "Net P&L": round2(pnl["Net P&L"])
    }
