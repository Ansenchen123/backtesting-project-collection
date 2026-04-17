from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

try:
    from tvDatafeed import Interval, TvDatafeed
except ImportError:  # pragma: no cover - runtime fallback
    Interval = None
    TvDatafeed = None
    import yfinance as yf


ROOT = Path(__file__).resolve().parent
OUTPUTS_DIR = ROOT / "outputs"


@dataclass
class StrategyConfig:
    symbol: str
    exchange: str = "TWSE"
    years: int = 8
    initial_cash: float = 1_000_000
    evaluation_years: int = 3
    initial_shares_pct: int = 50
    add_shares_multiplier: float = 0.8
    stoploss_pct: float = 4.5


def fetch_history(symbol: str, exchange: str, years: int) -> pd.DataFrame:
    if TvDatafeed is not None and Interval is not None:
        tv = TvDatafeed()
        data = tv.get_hist(
            symbol=symbol,
            exchange=exchange,
            n_bars=years * 240,
            interval=Interval.in_daily,
        )
        if data is None or data.empty:
            raise RuntimeError(f"Unable to fetch history for {symbol} on {exchange}.")
        data.index = pd.to_datetime(data.index)
        data.index.name = "Date"
        frame = data[["open", "high", "low", "close"]].rename(
            columns={"open": "Open", "high": "High", "low": "Low", "close": "Close"}
        )
    else:
        ticker = f"{symbol}.TW" if exchange == "TWSE" else symbol
        data = yf.download(ticker, period=f"{years}y", interval="1d", auto_adjust=False, progress=False)
        if data is None or data.empty:
            raise RuntimeError(f"Unable to fetch history for {ticker} from yfinance fallback.")
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        frame = data.rename(columns={"Open": "Open", "High": "High", "Low": "Low", "Close": "Close"})
        frame = frame[["Open", "High", "Low", "Close"]]
        frame.index.name = "Date"

    frame["20MA"] = frame["Close"].rolling(window=20).mean()
    frame["60MA"] = frame["Close"].rolling(window=60).mean()
    return frame


def run_strategy(config: StrategyConfig) -> tuple[pd.DataFrame, dict]:
    frame = fetch_history(config.symbol, config.exchange, config.years)
    cash = float(config.initial_cash)
    shares = 0
    last_buy_price = 0.0
    last_buy_shares = 0
    endday = config.evaluation_years * 240
    stoploss = config.stoploss_pct / 100
    transactions: list[dict] = []

    for i in range(len(frame) - endday):
        if i < 60:
            continue

        close_price = float(frame["Close"].iloc[i])
        date = frame.index[i]

        crossed_up = frame["20MA"].iloc[i - 1] < frame["60MA"].iloc[i - 1] and frame["20MA"].iloc[i] > frame["60MA"].iloc[i]
        crossed_down = frame["20MA"].iloc[i - 1] > frame["60MA"].iloc[i - 1] and frame["20MA"].iloc[i] < frame["60MA"].iloc[i]

        if crossed_up:
            buy_shares = int((cash * (config.initial_shares_pct / 100)) / close_price)
            total_cost = buy_shares * close_price * (1 + 0.001425)
            if buy_shares > 0 and cash >= total_cost:
                cash -= total_cost
                shares += buy_shares
                last_buy_price = close_price
                last_buy_shares = buy_shares
                transactions.append(
                    {
                        "Date": date,
                        "Type": "Buy",
                        "Shares": buy_shares,
                        "Price": close_price,
                        "Cash": cash,
                        "Net": cash + shares * close_price,
                    }
                )

        if shares > 0 and close_price > last_buy_price * 1.1:
            add_shares = int(last_buy_shares * config.add_shares_multiplier)
            total_cost = add_shares * close_price * (1 + 0.001425)
            if add_shares > 0 and cash >= total_cost:
                cash -= total_cost
                shares += add_shares
                last_buy_price = close_price
                last_buy_shares = add_shares
                transactions.append(
                    {
                        "Date": date,
                        "Type": "Add",
                        "Shares": add_shares,
                        "Price": close_price,
                        "Cash": cash,
                        "Net": cash + shares * close_price,
                    }
                )

        stoploss_triggered = shares > 0 and close_price < last_buy_price * (1 - stoploss)
        if shares > 0 and (crossed_down or stoploss_triggered):
            sell_shares = shares
            cash += sell_shares * close_price * (1 - 0.004425)
            shares = 0
            transactions.append(
                {
                    "Date": date,
                    "Type": "Sell",
                    "Shares": sell_shares,
                    "Price": close_price,
                    "Cash": cash,
                    "Net": cash,
                }
            )

    transactions_df = pd.DataFrame(transactions)
    if transactions_df.empty:
        raise RuntimeError("Strategy produced no transactions. Try a different symbol or date range.")

    transactions_df["PeakNet"] = transactions_df["Net"].cummax()
    transactions_df["Drawdown"] = (
        (transactions_df["PeakNet"] - transactions_df["Net"]) / transactions_df["PeakNet"]
    )

    max_drawdown = float(transactions_df["Drawdown"].max())
    initial_net = float(transactions_df.iloc[0]["Net"])
    final_net = float(transactions_df.iloc[-1]["Net"])
    total_return_pct = ((final_net - config.initial_cash) / config.initial_cash) * 100
    metrics = {
        "initial_cash": config.initial_cash,
        "initial_net": initial_net,
        "final_net": final_net,
        "total_return_pct": total_return_pct,
        "annualized_return_pct": total_return_pct / config.years,
        "max_drawdown_pct": max_drawdown * 100,
        "trade_count": int(len(transactions_df)),
    }
    return transactions_df, metrics


def save_outputs(config: StrategyConfig, trades: pd.DataFrame, metrics: dict) -> None:
    OUTPUTS_DIR.mkdir(exist_ok=True)
    trades.to_csv(OUTPUTS_DIR / f"{config.symbol}_transactions.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame([metrics]).to_csv(
        OUTPUTS_DIR / f"{config.symbol}_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(trades["Date"], trades["Net"], label="Net Asset Value")
    ax.plot(trades["Date"], trades["PeakNet"], label="Peak NAV", linestyle="--")
    ax.set_title(f"{config.symbol} TB Strategy Equity Curve")
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / f"{config.symbol}_equity_curve.png", dpi=150)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the TB strategy backtest.")
    parser.add_argument("--symbol", default="2330")
    parser.add_argument("--exchange", default="TWSE")
    parser.add_argument("--years", type=int, default=8)
    parser.add_argument("--cash", type=float, default=1_000_000)
    parser.add_argument("--evaluation-years", type=int, default=3)
    parser.add_argument("--initial-shares-pct", type=int, default=50)
    parser.add_argument("--add-shares-multiplier", type=float, default=0.8)
    parser.add_argument("--stoploss-pct", type=float, default=4.5)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = StrategyConfig(
        symbol=args.symbol,
        exchange=args.exchange,
        years=args.years,
        initial_cash=args.cash,
        evaluation_years=args.evaluation_years,
        initial_shares_pct=args.initial_shares_pct,
        add_shares_multiplier=args.add_shares_multiplier,
        stoploss_pct=args.stoploss_pct,
    )
    trades, metrics = run_strategy(config)
    save_outputs(config, trades, metrics)

    print(f"TB strategy completed for {config.symbol}.")
    print(f"Final net asset: {metrics['final_net']:.2f}")
    print(f"Total return: {metrics['total_return_pct']:.2f}%")
    print(f"Annualized return: {metrics['annualized_return_pct']:.2f}%")
    print(f"Max drawdown: {metrics['max_drawdown_pct']:.2f}%")
    print(f"Outputs written to: {OUTPUTS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
