import pytest
from core.utils import validate_inputs, round2

def test_round2():
    assert round2(12.345) == 12.35
    assert round2(0) == 0.00

def test_validate_inputs_valid():
    validate_inputs(100, 101, 10, "NSE")  # Should not raise

def test_validate_inputs_invalid_price():
    with pytest.raises(ValueError):
        validate_inputs(-1, 101, 10, "NSE")

def test_validate_inputs_invalid_quantity():
    with pytest.raises(ValueError):
        validate_inputs(100, 101, 0, "BSE")

def test_validate_inputs_invalid_exchange():
    with pytest.raises(ValueError):
        validate_inputs(100, 101, 10, "NYSE")
