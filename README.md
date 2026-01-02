# Zerodha Intraday P&L Calculator (Desktop App)

A modern desktop-based Zerodha intraday profit & loss calculator built with Python and Tkinter.  
The application provides accurate charge breakdowns, net P&L computation, and a clean GUI for quick intraday trade evaluation.

Designed with production-grade engineering principles: modularity, testability, and maintainability.

---

## Features

- Accurate Zerodha intraday P&L calculation
- Detailed breakdown of brokerage and statutory charges
- Net P&L and break-even point calculation
- Portfolio-level net P&L aggregation
- Desktop GUI using Tkinter and ttkbootstrap
- Fully unit-tested core logic using pytest
- Packaged as a standalone Windows executable using PyInstaller

---

## Project Structure

```text
zerodha_pnl_app/
├── core/
│   ├── calculator.py      # Pure business logic
│   ├── constants.py       # Centralized charge constants
│   └── utils.py           # Validation and helpers
│
├── gui.py                 # Desktop UI layer
├── main.py                # Application entry point
│
├── assets/
│   └── app.ico            # Application icon
│
├── tests/
│   ├── test_calculator.py
│   └── test_utils.py
│
├── ZerodhaPnL.spec        # PyInstaller configuration
├── requirements.txt
└── README.md
```

---

## Engineering Principles Used

- **Modularity**: UI, business logic, and constants are cleanly separated
- **Single Responsibility**: Each module does one job
- **Pure Functions**: Core P&L calculations have no side effects
- **Validation**: Strict input validation with clear error messages
- **Maintainability**: Constants centralized, readable logic
- **Testability**: Core logic fully unit tested
- **Scalability**: Easy to extend for delivery or F&O modules

---

## Desktop UI Highlights

- Clean and modern fixed-size layout
- Instant P&L calculation
- Color-coded profit and loss
- Portfolio-level aggregation for multiple trades

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip

### Install Dependencies

```bash
pip install -r requirements.txt
```

> Note: tkinter comes bundled with standard Python installations.

### Run the Application

```bash
python main.py
```

---

## Running Tests

```bash
pytest
```

---

## Build Standalone Executable (Windows)

```bash
pyinstaller ZerodhaPnL.spec
```

The executable will be generated in the `dist/` directory.

---

## Calculation Scope

- Intraday equity trades only
- Supported exchanges: **NSE**, **BSE**
- Charges aligned with Zerodha’s published pricing model

This tool is intended for educational and estimation purposes only.  
Actual charges may vary slightly due to broker or regulatory updates.

---

## Future Enhancements

- Delivery (CNC) trades
- Futures and Options support
- CSV trade import
- Trade history and analytics
- Dark mode
- Mac and Linux builds

---

## License

This project is open for learning and personal use.  
You may fork, modify, and extend it for non-commercial purposes.

---

## Author

**Chetan Maikhuri**  
Quality Engineering | Automation | Systems Thinking
