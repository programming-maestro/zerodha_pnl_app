import os
import json
import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import (
    Style, Frame, Label, Entry, Button, Combobox, Separator
)
from core.calculator import zerodha_intraday_pnl

APP_WIDTH = 800
APP_HEIGHT = 560
STATE_FILE = "app_state.json"
APP_ICON = os.path.join("assets", "app.ico")

# ================= Helpers =================
def format_inr(value):
    neg = value < 0
    value = abs(int(round(value)))
    s = str(value)
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts) + "," + tail
    return f"-₹ {s}" if neg else f"₹ {s}"

def center_window(root):
    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - APP_WIDTH) // 2
    y = (sh - APP_HEIGHT) // 2
    root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}")

# ================= Persistence =================
class AppState:
    @staticmethod
    def load():
        if not os.path.exists(STATE_FILE):
            return {"theme": "light", "trades": [], "window": None}
        with open(STATE_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save(state):
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)

# ================= App =================
class ZerodhaPnLApp:
    def __init__(self, root):
        self.root = root
        self.state = AppState.load()
        self.trades = self.state["trades"]
        self.calculated = False
        self.last_result = None

        self.style = Style(
            "flatly" if self.state["theme"] == "light" else "darkly"
        )

        self.root.title("Zerodha Intraday P&L")
        self.root.resizable(False, False)

        # Window positioning
        if self.state.get("window"):
            w = self.state["window"]
            self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{w['x']}+{w['y']}")
        else:
            center_window(self.root)

        # App icon
        if os.path.exists(APP_ICON):
            try:
                self.root.iconbitmap(APP_ICON)
            except Exception:
                pass

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self._build_ui()
        self._render_trades()

    # ================= UI =================
    def _build_ui(self):
        main = Frame(self.root)
        main.pack(fill="both", expand=True)

        self.left = Frame(main, padding=16)
        self.left.pack(side="left", fill="y")

        Separator(main, orient="vertical").pack(side="left", fill="y", padx=6)

        self.right = Frame(main, padding=16)
        self.right.pack(side="right", fill="both", expand=True)

        self._build_calculator()
        self._build_right_panel()

    # ================= Calculator =================
    def _build_calculator(self):
        Label(self.left, text="Calculator", font=("Segoe UI", 18, "bold")).pack(pady=(0, 12))

        self.buy = self._field("Buy Price")
        self.sell = self._field("Sell Price")
        self.qty = self._field("Quantity")

        Label(self.left, text="Exchange", font=("Segoe UI", 11)).pack(anchor="w")
        self.exchange = Combobox(self.left, values=["NSE", "BSE"], state="readonly")
        self.exchange.current(0)
        self.exchange.pack(fill="x", pady=6)

        self.pnl = Label(self.left, text="₹ 0", font=("Segoe UI", 24, "bold"))
        self.pnl.pack(pady=16)

        Button(self.left, text="Calculate", bootstyle="success",
               command=self.calculate).pack(fill="x", pady=4)

        self.add_btn = Button(self.left, text="Add Trade", bootstyle="primary",
                              state="disabled", command=self.add_trade)
        self.add_btn.pack(fill="x", pady=4)

    def _field(self, label):
        Label(self.left, text=label, font=("Segoe UI", 11)).pack(anchor="w")
        e = Entry(self.left, font=("Segoe UI", 11))
        e.pack(fill="x", pady=4)
        return e

    # ================= Right Panel =================
    def _build_right_panel(self):
        header = Frame(self.right)
        header.pack(fill="x", pady=(0, 8))

        Label(header, text="Saved Trades", font=("Segoe UI", 18, "bold")).pack(side="left")



        Button(
            header,
            text="🌗",
            width=3,
            command=self.toggle_theme
        ).pack(side="right")

        self.total_label = Label(
            self.right,
            text="Overall P&L: ₹ 0",
            font=("Segoe UI", 14, "bold")
        )
        self.total_label.pack(anchor="w", pady=(6, 10))

        # Scrollable trades area
        container = Frame(self.right)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scroll_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self._build_trades_grid()

        # Footer actions
        footer = Frame(self.right)
        footer.pack(fill="x", pady=(12, 0))

        Button(
            footer,
            text="Clear all trades",
            bootstyle="secondary",
            command=self.reset_trades
        ).pack(side="right")

    # ================= Trades Grid =================
    def _build_trades_grid(self):
        headers = ["BUY", "SELL", "QTY", "NET P&L", "CUMULATIVE", ""]
        for c, h in enumerate(headers):
            Label(self.scroll_frame, text=h, font=("Segoe UI", 11, "bold"))\
                .grid(row=0, column=c, padx=10, pady=6, sticky="w")

        Separator(self.scroll_frame).grid(row=1, column=0, columnspan=6, sticky="ew")

    def _render_trades(self):
        for w in self.scroll_frame.grid_slaves():
            if int(w.grid_info()["row"]) > 1:
                w.destroy()

        cumulative = 0
        total = 0
        row = 2

        for i, t in enumerate(self.trades):
            cumulative += t["net_pnl"]
            total += t["net_pnl"]

            Label(self.scroll_frame, text=t["buy"], font=("Segoe UI", 11)).grid(row=row, column=0, padx=10, sticky="w")
            Label(self.scroll_frame, text=t["sell"], font=("Segoe UI", 11)).grid(row=row, column=1, padx=10, sticky="w")
            Label(self.scroll_frame, text=t["qty"], font=("Segoe UI", 11)).grid(row=row, column=2, padx=10, sticky="w")

            Label(
                self.scroll_frame,
                text=format_inr(t["net_pnl"]),
                font=("Segoe UI", 11, "bold"),
                foreground="#1e8449" if t["net_pnl"] >= 0 else "#c0392b"
            ).grid(row=row, column=3, padx=10, sticky="w")

            Label(
                self.scroll_frame,
                text=format_inr(cumulative),
                font=("Segoe UI", 11, "bold"),
                foreground="#1e8449" if cumulative >= 0 else "#c0392b"
            ).grid(row=row, column=4, padx=10, sticky="w")

            self._delete_icon(self.scroll_frame, row, 5, i)

            Separator(self.scroll_frame).grid(row=row + 1, column=0, columnspan=6, sticky="ew", pady=6)
            row += 2

        self.total_label.config(
            text=f"Overall P&L: {format_inr(total)}",
            foreground="#1e8449" if total >= 0 else "#c0392b"
        )

    # ================= Circular Delete Icon =================
    def _delete_icon(self, parent, row, col, index):
        canvas = tk.Canvas(parent, width=24, height=24, highlightthickness=0, bd=0)
        canvas.grid(row=row, column=col, padx=6)
        canvas.create_oval(2, 2, 22, 22, fill="#c0392b", outline="")
        canvas.create_text(12, 12, text="×", fill="white",
                           font=("Segoe UI", 13, "bold"))
        canvas.bind("<Button-1>", lambda e: self.confirm_delete(index))

    # ================= Actions =================
    def calculate(self):
        try:
            buy = float(self.buy.get())
            sell = float(self.sell.get())
            qty = int(self.qty.get())

            if buy <= 0 or sell <= 0 or qty <= 0:
                raise ValueError

            self.last_result = zerodha_intraday_pnl(buy, sell, qty, self.exchange.get())
            net = self.last_result["Net P&L"]

            self.pnl.config(
                text=format_inr(net),
                foreground="#1e8449" if net >= 0 else "#c0392b"
            )

            self.calculated = True
            self.add_btn.config(state="normal")

        except Exception:
            messagebox.showerror("Invalid input", "Buy, Sell and Quantity must be greater than zero.")

    def add_trade(self):
        if not self.calculated or not self.last_result:
            return

        self.trades.append({
            "buy": int(float(self.buy.get())),
            "sell": int(float(self.sell.get())),
            "qty": int(self.qty.get()),
            "net_pnl": int(round(self.last_result["Net P&L"]))
        })

        self._persist()
        self._render_trades()

        self.calculated = False
        self.add_btn.config(state="disabled")

    def confirm_delete(self, index):
        if messagebox.askyesno("Confirm delete", "Delete this trade?"):
            self.trades.pop(index)
            self._persist()
            self._render_trades()

    def reset_trades(self):
        if messagebox.askyesno("Reset trades", "Remove all saved trades?"):
            self.trades.clear()
            self._persist()
            self._render_trades()

    def toggle_theme(self):
        self.state["theme"] = "dark" if self.state["theme"] == "light" else "light"
        self._persist()
        self.style.theme_use(
            "darkly" if self.state["theme"] == "dark" else "flatly"
        )

    def on_close(self):
        self.state["window"] = {
            "x": self.root.winfo_x(),
            "y": self.root.winfo_y()
        }
        self._persist()
        self.root.destroy()

    def _persist(self):
        AppState.save({
            "theme": self.state["theme"],
            "trades": self.trades,
            "window": self.state.get("window")
        })

# ================= Entry =================
def main():
    root = tk.Tk()
    ZerodhaPnLApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
