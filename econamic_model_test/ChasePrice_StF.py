from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class TradeRecord:
    date: str
    action: str
    shares: int
    price: float
    cash_after: float
    position_after: int
    equity_after: float


def chase_price_stf(
    data: pd.DataFrame,
    cash_initial: float = 100_000,
    fee_rate: float = 0.001425,
    tax_rate: float = 0.003,
    buy_fraction: float = 0.5,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    frame = data.copy()
    frame["Prev_Close"] = frame["Close"].shift(1).fillna(frame.iloc[0]["Close"])
    frame["Position"] = 0
    frame["Cash"] = 0.0
    frame["Equity"] = 0.0

    cash = float(cash_initial)
    position = 0
    adaptive_buy_fraction = buy_fraction
    records: List[TradeRecord] = []

    for timestamp, row in frame.iterrows():
        price = float(row["Close"])
        prev_close = float(row["Prev_Close"])
        shares_to_buy = int((cash * adaptive_buy_fraction) // (price * (1 + fee_rate)))

        if price > prev_close and shares_to_buy > 0:
            gross_cost = shares_to_buy * price
            total_cost = gross_cost * (1 + fee_rate)
            cash -= total_cost
            position += shares_to_buy
            adaptive_buy_fraction *= 0.5
            action = "BUY"
            records.append(
                TradeRecord(
                    date=str(timestamp.date()),
                    action=action,
                    shares=shares_to_buy,
                    price=price,
                    cash_after=cash,
                    position_after=position,
                    equity_after=cash + position * price,
                )
            )
        elif price < prev_close and position > 0:
            gross_revenue = price * position
            total_revenue = gross_revenue * (1 - fee_rate - tax_rate)
            shares_sold = position
            cash += total_revenue
            position = 0
            adaptive_buy_fraction = buy_fraction
            records.append(
                TradeRecord(
                    date=str(timestamp.date()),
                    action="SELL",
                    shares=shares_sold,
                    price=price,
                    cash_after=cash,
                    position_after=position,
                    equity_after=cash,
                )
            )

        frame.loc[timestamp, "Position"] = position
        frame.loc[timestamp, "Cash"] = cash
        frame.loc[timestamp, "Equity"] = cash + position * price

    total_value = float(cash + position * frame.iloc[-1]["Close"])
    total_return = ((total_value - cash_initial) / cash_initial) if cash_initial else 0.0
    peak_equity = frame["Equity"].cummax()
    drawdown = (frame["Equity"] - peak_equity) / peak_equity.replace(0, pd.NA)
    max_drawdown = float(drawdown.min()) if not drawdown.dropna().empty else 0.0

    trades = pd.DataFrame([record.__dict__ for record in records])
    metrics = {
        "initial_cash": float(cash_initial),
        "final_equity": total_value,
        "total_return_pct": total_return * 100,
        "max_drawdown_pct": abs(max_drawdown) * 100,
        "trade_count": int(len(trades)),
    }
    return frame, trades, metrics
