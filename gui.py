import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import (
    Style,
    Frame,
    Label,
    Entry,
    Button,
    Combobox,
    Treeview,
)

from core.calculator import zerodha_intraday_pnl


# ---------- Helpers ----------
def format_inr(value: float) -> str:
    neg = value < 0
    value = int(round(abs(value)))

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


class ZerodhaPnLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zerodha Intraday P&L Calculator")
        self.root.geometry("420x530") # change container length
        self.root.resizable(False, False)

        self.portfolio = []

        self._build_background()
        self._build_ui()

    # ================= Background =================
    def _build_background(self):
        canvas = tk.Canvas(self.root, width=420, height=530, highlightthickness=0) # change container length
        canvas.place(x=0, y=0)

        r1, g1, b1 = self.root.winfo_rgb("#0f2027")
        r2, g2, b2 = self.root.winfo_rgb("#2c5364")

        for i in range(680):
            r = int(r1 + (r2 - r1) * i / 530)
            g = int(g1 + (g2 - g1) * i / 530)
            b = int(b1 + (b2 - b1) * i / 530)
            color = f"#{r//256:02x}{g//256:02x}{b//256:02x}"
            canvas.create_line(0, i, 420, i, fill=color)

    # ================= UI =================
    def _build_ui(self):
        panel = Frame(self.root, padding=12, bootstyle="light")
        panel.place(x=10, y=10, width=400, height=510) # change cantainer length

        # ---------- Net P&L ----------
        Label(
            panel,
            text="Net P&L",
            font=("Segoe UI Semibold", 20),
            foreground="#2c5877",
        ).pack()
        self.pnl_value = Label(
            panel,
            text="₹ 0",
            font=("Segoe UI", 18, "bold"),
            foreground="#34495e",
        )
        self.pnl_value.pack(pady=(0, 4))

        # ---------- Inputs ----------
        form = Frame(panel, padding=6)
        form.pack(fill="x")

        self.buy_entry = self._field(form, "Buy Price (₹)", 0)
        self.sell_entry = self._field(form, "Sell Price (₹)", 1)
        self.qty_entry = self._field(form, "Quantity", 2)

        Label(form, text="Exchange").grid(row=3, column=0, sticky="w", pady=1)
        self.exchange_combo = Combobox(form, values=["NSE", "BSE"], state="readonly")
        self.exchange_combo.current(0)
        self.exchange_combo.grid(row=3, column=1, sticky="ew", padx=4)

        form.columnconfigure(1, weight=1)

        # ---------- Buttons (NO GAP) ----------
        btns = Frame(panel)
        btns.pack(fill="x")

        Button(btns, text="Calculate", bootstyle="success", command=self.calculate)\
            .pack(side="left", expand=True, padx=2)
        Button(btns, text="Add", bootstyle="primary", command=self.add_to_portfolio)\
            .pack(side="left", expand=True, padx=2)
        Button(btns, text="Reset", bootstyle="secondary", command=self.reset)\
            .pack(side="left", expand=True, padx=2)

        # ---------- Results (FIXED, NO SCROLL) ----------
        self.table = Treeview(
            panel,
            columns=("Metric", "Value"),
            show="headings",
            height=12,   # key change
        )
        self.table.heading("Metric", text="Metric")
        self.table.heading("Value", text="Value")
        self.table.column("Metric", width=220, anchor="w")
        self.table.column("Value", width=130, anchor="e")
        self.table.pack(pady=(2, 2))

        # ---------- Portfolio ----------

        self.portfolio_label = Label(
            panel,
            text="Portfolio Net P&L",
            font=("Segoe UI Semibold", 15),
            foreground="#3b6a8f",
        )

        self.portfolio_value = Label(
            panel,
            text="₹ 0",
            font=("Segoe UI", 18, "bold"),
            foreground="#2c3e50",
        )

        self.portfolio_label.pack(pady=(2, 0))

    def _field(self, parent, label, row):
        Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=1)
        e = Entry(parent)
        e.grid(row=row, column=1, sticky="ew", padx=4)
        return e

    # ================= Actions =================
    def calculate(self):
        try:
            r = self._calc()
            self._render(r)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_to_portfolio(self):
        try:
            r = self._calc()
            self.portfolio.append(r["Net P&L"])
            self._render_portfolio()
            self._render(r)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reset(self):
        for e in (self.buy_entry, self.sell_entry, self.qty_entry):
            e.delete(0, tk.END)
        self.table.delete(*self.table.get_children())
        self.pnl_value.config(text="₹ 0", foreground="#34495e")
        self.portfolio.clear()
        self._render_portfolio()

    # ================= Rendering =================
    def _calc(self):
        return zerodha_intraday_pnl(
            float(self.buy_entry.get()),
            float(self.sell_entry.get()),
            int(self.qty_entry.get()),
            self.exchange_combo.get(),
        )

    def _render(self, result):
        self.table.delete(*self.table.get_children())

        net = result["Net P&L"]
        self.pnl_value.config(
            text=format_inr(net),
            foreground="#1e8449" if net >= 0 else "#c0392b",
        )

        for k, v in result.items():
            self.table.insert("", "end", values=(k, format_inr(v)))

    def _render_portfolio(self):
        total = sum(self.portfolio)
        self.portfolio_label.config(
            text=f"Portfolio Net P&L: {format_inr(total)}",
            foreground="#1e8449" if total >= 0 else "#c0392b",
        )


def main():
    style = Style("flatly")
    root = style.master
    ZerodhaPnLApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
