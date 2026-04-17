from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent
OUTPUTS_DIR = ROOT / "outputs"


def simulate_trading(
    price_file: Path,
    signal_file: Path,
    start_date: str,
    initial_cash: float = 10_000,
    fee_rate: float = 0.003,
    putcash_mode: float = 0.2,
) -> pd.DataFrame:
    df_price = pd.read_excel(price_file)
    df_signal = pd.read_excel(signal_file)

    df_price["Date"] = pd.to_datetime(df_price["Date"]).dt.normalize()
    signal_date_column = "Date" if "Date" in df_signal.columns else df_signal.columns[0]
    signal_category_column = next(
        (col for col in df_signal.columns if "prediction" in str(col).lower()),
        df_signal.columns[-1],
    )
    df_signal["Date"] = pd.to_datetime(df_signal[signal_date_column]).dt.normalize()
    df_signal["Category"] = df_signal[signal_category_column].astype(str).str.strip()

    cash = float(initial_cash)
    stock = 0
    peak_value = initial_cash
    portfolio_history = []
    horizontal_line = []
    holding = False
    consecutive_positive = 0
    last_signal = ""

    current_date = pd.to_datetime(start_date)
    last_date = df_signal["Date"].max()

    while current_date <= last_date:
        signal_row = df_signal[df_signal["Date"] == current_date]
        price_row = df_price[df_price["Date"] == current_date]

        if signal_row.empty or price_row.empty:
            current_date += pd.DateOffset(days=1)
            continue

        category = signal_row["Category"].iloc[0] or last_signal
        price = float(price_row["Close"].iloc[0])
        total_assets = cash + stock * price
        peak_value = max(peak_value, total_assets)

        if holding and total_assets <= initial_cash * 0.5:
            cash += stock * price * (1 - fee_rate)
            stock = 0
            holding = False
            consecutive_positive = 0

        if category.lower().startswith("bear") and stock > 0:
            cash += stock * price * (1 - fee_rate)
            stock = 0
            holding = False
            consecutive_positive = 0
        elif category.lower().startswith("bull"):
            consecutive_positive += 1
            invest_ratio = min(putcash_mode * consecutive_positive, 1.0)
            buy_cash = cash * invest_ratio
            buy_shares = int(buy_cash / (price * (1 + fee_rate)))
            total_cost = price * buy_shares * (1 + fee_rate)
            if buy_shares > 0 and cash >= total_cost:
                stock += buy_shares
                cash -= total_cost
                holding = True

        color = None
        if category.lower().startswith("bull"):
            color = "darkred"
        elif category.lower().startswith("bear"):
            color = "darkgreen"
        if color:
            horizontal_line.append((current_date, color))

        total_assets = cash + stock * price
        portfolio_history.append(
            {
                "Date": current_date,
                "Cash": cash,
                "Stock": stock,
                "Price": price,
                "TotalAssets": total_assets,
                "PeakAssets": peak_value,
                "DrawdownPct": ((peak_value - total_assets) / peak_value) * 100 if peak_value else 0,
                "Signal": category,
            }
        )

        last_signal = category
        current_date += pd.DateOffset(days=1)

    result = pd.DataFrame(portfolio_history)
    result.attrs["horizontal_line"] = horizontal_line
    return result


def save_outputs(result: pd.DataFrame, output_name: str) -> None:
    OUTPUTS_DIR.mkdir(exist_ok=True)
    csv_path = OUTPUTS_DIR / f"{output_name}_trading_log.csv"
    result.to_csv(csv_path, index=False)

    plt.figure(figsize=(12, 6))
    plt.plot(result["Date"], result["TotalAssets"], label="Strategy Total Assets", linewidth=2)
    plt.plot(
        result["Date"],
        result["Price"] / result["Price"].iloc[0] * result["TotalAssets"].iloc[0],
        label="Buy and Hold",
        color="red",
        linestyle="--",
    )

    y_level = result["TotalAssets"].max() * 0.25
    for dt, color in result.attrs.get("horizontal_line", []):
        plt.hlines(y=y_level, xmin=dt, xmax=dt + pd.Timedelta(days=3), colors=color, linewidth=2)

    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.title(f"{output_name} Trading Simulation")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUTS_DIR / f"{output_name}_simulation.png", dpi=150)
    plt.close()

    summary = pd.DataFrame(
        [
            {
                "final_assets": float(result["TotalAssets"].iloc[-1]),
                "max_drawdown_pct": float(result["DrawdownPct"].max()),
                "rows": int(len(result)),
            }
        ]
    )
    summary.to_csv(OUTPUTS_DIR / f"{output_name}_summary.csv", index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the spreadsheet-driven trading simulation.")
    parser.add_argument("--dataset", choices=["google", "intel"], default="google")
    parser.add_argument("--start-date", default="2014-07-14")
    parser.add_argument("--cash", type=float, default=10_000)
    parser.add_argument("--fee-rate", type=float, default=0.003)
    parser.add_argument("--putcash-mode", type=float, default=0.5)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    price_file = ROOT / f"{args.dataset}_filtered_data.xlsx"
    signal_file = ROOT / f"{args.dataset}.xlsx"
    result = simulate_trading(
        price_file=price_file,
        signal_file=signal_file,
        start_date=args.start_date,
        initial_cash=args.cash,
        fee_rate=args.fee_rate,
        putcash_mode=args.putcash_mode,
    )
    save_outputs(result, args.dataset)
    print(f"Simulation completed for {args.dataset}.")
    print(f"Final assets: {result['TotalAssets'].iloc[-1]:.2f}")
    print(f"Max drawdown: {result['DrawdownPct'].max():.2f}%")
    print(f"Outputs written to: {OUTPUTS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
