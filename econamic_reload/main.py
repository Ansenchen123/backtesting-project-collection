from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from func import Account
from get_data import DataFetcher


ROOT = Path(__file__).resolve().parent
OUTPUTS_DIR = ROOT / "outputs"


def run_backtest(
    symbol: str,
    years: int,
    initial_cash: float,
    short_window: int,
    long_window: int,
    refresh_data: bool,
) -> tuple[pd.DataFrame, dict]:
    OUTPUTS_DIR.mkdir(exist_ok=True)
    account = Account("TestUser", cash=initial_cash, base_dir=OUTPUTS_DIR)
    fetcher = DataFetcher(years=years, cache_dir=OUTPUTS_DIR / "data_cache")
    data = fetcher.download_stock_data(symbol, refresh=refresh_data)
    frame = fetcher.iter_days()

    frame["ma_short"] = frame["close"].rolling(short_window).mean()
    frame["ma_long"] = frame["close"].rolling(long_window).mean()

    equity_records = []
    for _, row in frame.iterrows():
        if pd.isna(row["ma_short"]) or pd.isna(row["ma_long"]):
            account.write_account_snapshot(str(row["date"].date()), close_price=float(row["close"]))
            equity_records.append(
                {
                    "date": row["date"],
                    "close": row["close"],
                    "cash": account.cash,
                    "position": account.stock.get(symbol, 0),
                    "equity": account.cash + account.stock.get(symbol, 0) * row["close"],
                    "signal": "HOLD",
                }
            )
            account.day_off()
            continue

        signal = "HOLD"
        close_price = float(row["close"])

        if row["ma_short"] > row["ma_long"]:
            lots = (account.cash - account.total_debt) // (close_price * 100)
            quantity = int(lots * 100)
            if quantity > 0:
                account.buy(symbol, close_price, quantity)
                signal = "BUY"
        elif row["ma_short"] < row["ma_long"]:
            current_qty = account.stock.get(symbol, 0)
            if current_qty > 0:
                account.sell(symbol, close_price, current_qty)
                signal = "SELL"

        equity = account.cash + account.stock.get(symbol, 0) * close_price - account.total_debt
        account.write_account_snapshot(str(row["date"].date()), close_price=close_price)
        equity_records.append(
            {
                "date": row["date"],
                "close": close_price,
                "cash": account.cash,
                "position": account.stock.get(symbol, 0),
                "equity": equity,
                "signal": signal,
                "ma_short": row["ma_short"],
                "ma_long": row["ma_long"],
            }
        )
        account.day_off()

    equity_frame = pd.DataFrame(equity_records)
    if equity_frame.empty:
        raise RuntimeError("Backtest produced no records.")

    equity_frame.to_csv(OUTPUTS_DIR / f"{symbol}_equity_curve.csv", index=False)
    metrics = {
        "initial_cash": float(initial_cash),
        "final_equity": float(equity_frame.iloc[-1]["equity"]),
        "return_pct": ((equity_frame.iloc[-1]["equity"] - initial_cash) / initial_cash) * 100,
        "buy_count": int((equity_frame["signal"] == "BUY").sum()),
        "sell_count": int((equity_frame["signal"] == "SELL").sum()),
    }
    return equity_frame, metrics


def save_chart(symbol: str, frame: pd.DataFrame) -> None:
    plt.figure(figsize=(12, 6))
    plt.plot(frame["date"], frame["close"], label="Close Price")
    plt.plot(frame["date"], frame["equity"], label="Strategy Equity")
    plt.plot(frame["date"], frame["ma_short"], label="Short MA", alpha=0.8)
    plt.plot(frame["date"], frame["ma_long"], label="Long MA", alpha=0.8)
    plt.title(f"{symbol} Moving Average Backtest")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / f"{symbol}_backtest.png", dpi=150)
    plt.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a moving-average stock simulation.")
    parser.add_argument("--symbol", default="2330")
    parser.add_argument("--years", type=int, default=5)
    parser.add_argument("--cash", type=float, default=1_000_000)
    parser.add_argument("--short-window", type=int, default=20)
    parser.add_argument("--long-window", type=int, default=60)
    parser.add_argument("--refresh-data", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    frame, metrics = run_backtest(
        symbol=args.symbol,
        years=args.years,
        initial_cash=args.cash,
        short_window=args.short_window,
        long_window=args.long_window,
        refresh_data=args.refresh_data,
    )
    save_chart(args.symbol, frame)

    print(f"Simulation completed for {args.symbol}.")
    print(f"Initial cash: {metrics['initial_cash']:.2f}")
    print(f"Final equity: {metrics['final_equity']:.2f}")
    print(f"Return: {metrics['return_pct']:.2f}%")
    print(f"Buy signals executed: {metrics['buy_count']}")
    print(f"Sell signals executed: {metrics['sell_count']}")
    print(f"Outputs written to: {OUTPUTS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
