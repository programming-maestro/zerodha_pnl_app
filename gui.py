import tkinter as tk
from tkinter import ttk, messagebox
from core.calculator import zerodha_intraday_pnl


class ZerodhaPnLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zerodha Intraday P&L Calculator")
        self.root.geometry("540x600")
        self.root.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        tk.Label(self.root, text="📊 Zerodha Intraday P&L Calculator",
                 font=("Segoe UI", 14, "bold")).pack(pady=10)

        frame_inputs = tk.Frame(self.root)
        frame_inputs.pack(pady=10)

        # Input fields
        tk.Label(frame_inputs, text="Buy Price (₹):", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="e", pady=5)
        self.buy_entry = tk.Entry(frame_inputs, width=20)
        self.buy_entry.grid(row=0, column=1, padx=10)

        tk.Label(frame_inputs, text="Sell Price (₹):", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="e", pady=5)
        self.sell_entry = tk.Entry(frame_inputs, width=20)
        self.sell_entry.grid(row=1, column=1, padx=10)

        tk.Label(frame_inputs, text="Quantity:", font=("Segoe UI", 11)).grid(row=2, column=0, sticky="e", pady=5)
        self.qty_entry = tk.Entry(frame_inputs, width=20)
        self.qty_entry.grid(row=2, column=1, padx=10)

        tk.Label(frame_inputs, text="Exchange:", font=("Segoe UI", 11)).grid(row=3, column=0, sticky="e", pady=5)
        self.exchange_combo = ttk.Combobox(frame_inputs, values=["NSE", "BSE"], width=17, state="readonly")
        self.exchange_combo.current(0)
        self.exchange_combo.grid(row=3, column=1, padx=10)

        # Button
        tk.Button(self.root, text="Calculate P&L", font=("Segoe UI", 12, "bold"),
                  bg="#0078D7", fg="white", relief="raised", command=self.calculate_pnl).pack(pady=10)

        # Output Text Box
        self.output = tk.Text(self.root, width=60, height=20, font=("Consolas", 10))
        self.output.pack(pady=10)

        tk.Label(self.root, text="*Based on Zerodha Brokerage Calculator",
                 font=("Segoe UI", 9, "italic")).pack(side="bottom", pady=5)

    def calculate_pnl(self):
        try:
            buy = float(self.buy_entry.get())
            sell = float(self.sell_entry.get())
            qty = int(self.qty_entry.get())
            exch = self.exchange_combo.get()

            result = zerodha_intraday_pnl(buy, sell, qty, exch)

            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, f"Exchange: {exch}\n" + "-" * 40 + "\n")
            for k, v in result.items():
                self.output.insert(tk.END, f"{k:25s}: {v}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))
