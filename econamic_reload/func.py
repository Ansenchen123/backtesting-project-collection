from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path


@dataclass
class Account:
    name: str
    cash: float = 1_000_000
    stock: dict[str, int] = field(default_factory=dict)
    debt_1: float = 0
    debt_2: float = 0
    debt_3: float = 0
    base_dir: Path = Path(".")

    def __post_init__(self) -> None:
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.account_file = self.base_dir / "account.json"
        self.summary_file = self.base_dir / "account_summary.csv"
        self.persist()

    @property
    def total_debt(self) -> float:
        return self.debt_1 + self.debt_2 + self.debt_3

    def persist(self) -> None:
        payload = {
            "name": self.name,
            "cash": self.cash,
            "stock": self.stock,
            "debt_1": self.debt_1,
            "debt_2": self.debt_2,
            "debt_3": self.debt_3,
        }
        self.account_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def buy(self, stock_name: str, stock_price: float, quantity: int) -> None:
        raw_cost = stock_price * quantity
        fee = max(int(raw_cost * 0.001425), 20)
        self.debt_3 += int(raw_cost + fee)
        self.stock[stock_name] = int(self.stock.get(stock_name, 0) + quantity)

    def sell(self, stock_name: str, stock_price: float, quantity: int) -> None:
        if self.stock.get(stock_name, 0) < quantity:
            raise ValueError("Not enough stock to sell.")

        raw_revenue = stock_price * quantity
        fee = max(int(raw_revenue * 0.001425), 20)
        tax = int(raw_revenue * 0.003)
        self.debt_3 -= int(raw_revenue - fee - tax)
        self.stock[stock_name] -= quantity
        if self.stock[stock_name] == 0:
            del self.stock[stock_name]

    def day_off(self) -> None:
        self.cash -= self.debt_1
        self.debt_1 = self.debt_2
        self.debt_2 = self.debt_3
        self.debt_3 = 0
        if self.cash < 0:
            raise ValueError("Insufficient funds to cover debts.")
        self.persist()

    def write_account_snapshot(self, date_text: str, close_price: float | None = None) -> None:
        total_stock_value = 0.0
        if close_price is not None:
            total_stock_value = sum(quantity * close_price for quantity in self.stock.values())
        total_assets = self.cash + total_stock_value
        line = (
            f"{date_text},{self.cash:.2f},{json.dumps(self.stock, ensure_ascii=False)},"
            f"{self.debt_1:.2f},{self.debt_2:.2f},{self.debt_3:.2f},{total_assets:.2f}\n"
        )
        if not self.summary_file.exists():
            self.summary_file.write_text(
                "date,cash,stock,debt_1,debt_2,debt_3,total_assets\n",
                encoding="utf-8",
            )
        with self.summary_file.open("a", encoding="utf-8") as handle:
            handle.write(line)
