from __future__ import annotations

import argparse
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parent
VENDORED_TVDATAFEED = ROOT / "tvdatafeed-main"
OUTPUTS_DIR = ROOT / "outputs"

if str(VENDORED_TVDATAFEED) not in sys.path:
    sys.path.insert(0, str(VENDORED_TVDATAFEED))

try:
    from tvDatafeed import Interval, TvDatafeed
except Exception:  # pragma: no cover - fallback when vendored dependency is incomplete
    Interval = None
    TvDatafeed = None

from ChasePrice_StF import chase_price_stf


def fetch_history(symbol: str, exchange: str, interval: Interval | None, years: int) -> pd.DataFrame:
    if TvDatafeed is not None and Interval is not None:
        tv = TvDatafeed()
        bars = years * 240
        data = tv.get_hist(symbol=symbol, exchange=exchange, n_bars=bars, interval=interval)
        if data is None or data.empty:
            raise RuntimeError(f"Unable to fetch history for {symbol} on {exchange}.")
        data.index = pd.to_datetime(data.index)
        data.index.name = "Date"
        return data[["open", "high", "low", "close"]].rename(
            columns={"open": "Open", "high": "High", "low": "Low", "close": "Close"}
        )

    ticker = f"{symbol}.TW" if exchange == "TWSE" else symbol
    data = yf.download(ticker, period=f"{years}y", interval="1d", auto_adjust=False, progress=False)
    if data is None or data.empty:
        raise RuntimeError(f"Unable to fetch history for {ticker} from yfinance fallback.")
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data.index = pd.to_datetime(data.index)
    data.index.name = "Date"
    return data[["Open", "High", "Low", "Close"]]


def save_outputs(symbol: str, history: pd.DataFrame, strategy: pd.DataFrame, trades: pd.DataFrame) -> Path:
    OUTPUTS_DIR.mkdir(exist_ok=True)
    history.to_csv(OUTPUTS_DIR / f"{symbol.lower()}_history.csv")
    strategy.to_csv(OUTPUTS_DIR / f"{symbol.lower()}_equity_curve.csv")
    trades.to_csv(OUTPUTS_DIR / f"{symbol.lower()}_trades.csv", index=False)
    return OUTPUTS_DIR


def render_plot(symbol: str, strategy: pd.DataFrame, output_dir: Path, show_plot: bool) -> None:
    figure_path = output_dir / f"{symbol.lower()}_chart.png"
    plt.figure(figsize=(12, 6))
    plt.plot(strategy.index, strategy["Close"], label="Close Price")
    plt.plot(strategy.index, strategy["Equity"], label="Strategy Equity")
    plt.title(f"{symbol} Chase Price Strategy")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(figure_path, dpi=150)
    if show_plot:
        plt.show()
    plt.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the chase-price backtest for a Taiwan equity.")
    parser.add_argument("--symbol", default="2330", help="Ticker symbol. Default: 2330")
    parser.add_argument("--exchange", default="TWSE", help="Exchange name. Default: TWSE")
    parser.add_argument("--years", type=int, default=5, help="Lookback years. Default: 5")
    parser.add_argument(
        "--cash",
        type=float,
        default=100_000,
        help="Initial cash used by the strategy. Default: 100000",
    )
    parser.add_argument(
        "--show-plot",
        action="store_true",
        help="Open the matplotlib window in addition to saving the chart.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    history = fetch_history(
        symbol=args.symbol,
        exchange=args.exchange,
        interval=Interval.in_daily if Interval is not None else None,
        years=args.years,
    )
    strategy, trades, metrics = chase_price_stf(history, cash_initial=args.cash)
    output_dir = save_outputs(args.symbol, history, strategy, trades)
    render_plot(args.symbol, strategy, output_dir, args.show_plot)

    print(f"Backtest completed for {args.symbol}.")
    print(f"Initial cash: {metrics['initial_cash']:.2f}")
    print(f"Final equity: {metrics['final_equity']:.2f}")
    print(f"Total return: {metrics['total_return_pct']:.2f}%")
    print(f"Max drawdown: {metrics['max_drawdown_pct']:.2f}%")
    print(f"Trade count: {metrics['trade_count']}")
    print(f"Outputs written to: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
