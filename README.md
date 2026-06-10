# Backtesting Project Collection

This repository groups four independent Python experiments for stock-data loading, rule-based trading simulation, and spreadsheet-driven signal testing.

## How to Use This Collection

Work inside one subproject at a time. Each folder has its own requirements file, and each script creates its result directory at runtime. Some runs need network access for TradingView, Yahoo Finance, or FinMind market data.

## Subprojects

### `econamic_model_test`

Description:

- Runs a Taiwan equity chase-price backtest from `econamic_model_test/main.py`.
- Uses `econamic_model_test/ChasePrice_StF.py` for the trading rule: buy when the close rises from the previous close, reduce later buy size after each buy, and sell when the close falls.
- Attempts to use vendored TradingView access under `econamic_model_test/tvdatafeed-main/`; when that path is not usable, the script falls back to yfinance.
- Saves price history, the strategy equity curve, trade records, and a chart after the simulation completes.

Technology:

- Python
- pandas
- matplotlib
- yfinance
- vendored tvDatafeed source
- setuptools

Run from the collection root:

```powershell
cd econamic_model_test
pip install -r requirements.txt
python main.py --symbol 2330 --years 3 --cash 100000
```

### `econamic_reload`

Description:

- Runs a FinMind-backed moving-average simulation from `econamic_reload/main.py`.
- Uses `econamic_reload/get_data.py` to download or reuse cached Taiwan stock daily data.
- Uses `econamic_reload/func.py` to model cash, stock holdings, three-day debt settlement, account persistence, and daily account snapshots.
- Calculates short and long moving averages, executes buy and sell signals, then writes an equity curve and chart.

Technology:

- Python
- pandas
- FinMind
- matplotlib
- JSON account state
- CSV output

Run from the collection root:

```powershell
cd econamic_reload
pip install -r requirements.txt
python main.py --symbol 2330 --years 5
```

### `TB_Strategy`

Description:

- Runs a 20-day and 60-day moving-average crossover strategy from `TB_Strategy/TB_Strategy.py`.
- Fetches daily price history with tvDatafeed when available and falls back to yfinance when that import is unavailable.
- Buys on upward moving-average crosses, adds shares after strong price movement, and exits on downward crosses or stop-loss triggers.
- Saves transaction records, a summary file, and an equity-curve chart.

Technology:

- Python
- pandas
- matplotlib
- tvdatafeed
- yfinance
- setuptools

Run from the collection root:

```powershell
cd TB_Strategy
pip install -r requirements.txt
python TB_Strategy.py --symbol 2330 --years 5 --evaluation-years 2
```

### `PY_mod_econamic`

Description:

- Runs a spreadsheet-driven trading simulation from `PY_mod_econamic/return_test.py`.
- Reads signal workbooks `PY_mod_econamic/google.xlsx` or `PY_mod_econamic/intel.xlsx` and matching price workbooks `PY_mod_econamic/google_filtered_data.xlsx` or `PY_mod_econamic/intel_filtered_data.xlsx`.
- Buys after bullish signal rows, sells after bearish signal rows, applies a fee rate, tracks total assets, and compares the result with a buy-and-hold line in the chart.
- Includes `PY_mod_econamic/downloadXslx.py` as a separate TradingView-based helper for regenerating Google price data.

Technology:

- Python
- pandas
- openpyxl
- matplotlib
- Excel workbook inputs
- CSV and PNG output

Run from the collection root:

```powershell
cd PY_mod_econamic
pip install -r requirements.txt
python return_test.py --dataset google
```

The accepted dataset values are google and intel.

## Repository Layout

```text
backtesting-project-collection/
  econamic_model_test/
  econamic_reload/
  TB_Strategy/
  PY_mod_econamic/
  README.md
```

## Data and Output Notes

- The first three subprojects can request market data over the network.
- The spreadsheet-driven project can run from the included Excel files.
- Generated result folders are created by the scripts and are intentionally not required before running them.
- The folder names keep their original spelling so commands and links match the repository exactly.

## 摘要

- 本倉庫整理四個彼此獨立的 Python 回測與交易模擬子專案。
- `econamic_model_test` 使用追價規則測試台股資料，並可在 tvDatafeed 不可用時改用 yfinance。
- `econamic_reload` 使用 FinMind 資料與移動平均線訊號，同時模擬帳戶現金、持股與交割負債。
- `TB_Strategy` 測試 20 日與 60 日均線交叉、加碼與停損條件。
- `PY_mod_econamic` 使用內含 Excel 檔案進行訊號驅動的交易模擬，並輸出紀錄與圖表。
- 每個子專案都列出對應技術與執行方式，方便分別安裝依賴並單獨執行。
