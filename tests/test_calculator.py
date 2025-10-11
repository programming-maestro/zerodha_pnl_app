import pytest
from core.calculator import zerodha_intraday_pnl

def test_basic_intraday_nse():
    """Test normal NSE intraday trade"""
    result = zerodha_intraday_pnl(buy_price=100, sell_price=101, quantity=10, exchange="NSE")

    # Expected core numbers (based on Zerodha calculator)
    assert result["Turnover"] == 2010.00
    assert round(result["Zerodha Brokerage"], 2) == 0.6
    assert round(result["Total Charges"], 2) == pytest.approx(1.07, rel=1e-2)
    assert round(result["Net P&L"], 2) == pytest.approx(8.93, rel=1e-2)


def test_basic_intraday_bse():
    """Test normal BSE intraday trade"""
    result = zerodha_intraday_pnl(buy_price=100, sell_price=101, quantity=10, exchange="BSE")

    assert result["Turnover"] == 2010.00
    # BSE exchange txn charge slightly different
    assert result["Exchange Txn Charges"] != 0.06
    assert "Net P&L" in result


def test_invalid_exchange():
    """Ensure invalid exchange raises error"""
    with pytest.raises(ValueError):
        zerodha_intraday_pnl(100, 101, 10, "INVALID")


def test_invalid_prices():
    """Ensure negative or zero prices raise error"""
    with pytest.raises(ValueError):
        zerodha_intraday_pnl(0, 101, 10, "NSE")

    with pytest.raises(ValueError):
        zerodha_intraday_pnl(100, -5, 10, "BSE")
