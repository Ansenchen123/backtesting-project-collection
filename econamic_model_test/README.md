# econamic_model_test

`econamic_model_test` 是一個以台股為主的簡易回測專案，核心概念是使用追價策略觀察資金曲線與交易結果。

## 專案內容

- [main.py](F:\learndata\econamic_model_test\main.py)：命令列入口，負責下載歷史資料、執行回測並輸出結果
- [ChasePrice_StF.py](F:\learndata\econamic_model_test\ChasePrice_StF.py)：追價策略本體，包含交易紀錄與績效統計
- `tvdatafeed-main/`：專案內附的資料來源相依套件
- `outputs/`：回測後產生的歷史資料、權益曲線、交易紀錄與圖表

## 策略說明

這個專案的策略邏輯很單純：

- 當日收盤價高於前一日收盤價時，依照目前可用資金的一部分買進
- 如果價格持續上升，後續每次加碼的比例會逐步縮小
- 當價格跌回前一日收盤價以下時，全部賣出

此專案的目的不是建立完整交易系統，而是保留一個清楚、可重現的策略回測範例。

## 安裝需求

- Python 3.10 以上
- [requirements.txt](F:\learndata\econamic_model_test\requirements.txt) 內列出的套件

安裝方式：

```bash
pip install -r requirements.txt
```

## 執行方式

使用預設參數執行：

```bash
python main.py
```

指定股票與回測年數：

```bash
python main.py --symbol 2330 --years 3 --cash 100000
```

可用參數：

- `--symbol`：股票代號，預設為 `2330`
- `--exchange`：交易所名稱，預設為 `TWSE`
- `--years`：抓取歷史資料的年數
- `--cash`：初始資金
- `--show-plot`：執行後額外開啟圖表視窗

## 輸出內容

每次執行後會在 [outputs](F:\learndata\econamic_model_test\outputs) 產生：

- `*_history.csv`：歷史價格資料
- `*_equity_curve.csv`：策略資金曲線
- `*_trades.csv`：交易紀錄
- `*_chart.png`：收盤價與策略權益曲線圖

## 備註

- 專案保留了內附的 `tvdatafeed-main`，同時也有 `yfinance` fallback，降低環境相依問題
- `outputs/`、虛擬環境與暫存檔都應維持不追蹤
