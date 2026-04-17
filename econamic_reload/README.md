# econamic_reload

`econamic_reload` 是一個以均線交叉為核心的台股模擬交易專案，主要用來觀察長短期移動平均下的買賣結果。

## 專案內容

- [main.py](F:\learndata\econamic_reload\main.py)：回測入口
- [get_data.py](F:\learndata\econamic_reload\get_data.py)：資料下載與快取邏輯
- [func.py](F:\learndata\econamic_reload\func.py)：帳戶、負債與每日結算處理
- `outputs/`：快取資料、帳戶快照、資金曲線與圖表

## 策略說明

此專案的核心邏輯為：

- 短均線高於長均線時買進
- 短均線低於長均線時全部賣出

專案同時保留帳戶、持股、交割延遲與每日結算概念，讓它不只是單純的「資產曲線計算器」。

## 安裝需求

- Python 3.10 以上
- [requirements.txt](F:\learndata\econamic_reload\requirements.txt) 內列出的套件

安裝方式：

```bash
pip install -r requirements.txt
```

## 執行方式

使用預設參數：

```bash
python main.py
```

指定股票、均線與資金：

```bash
python main.py --symbol 2330 --years 8 --cash 1500000 --short-window 10 --long-window 30
```

可用參數：

- `--symbol`：股票代號
- `--years`：歷史資料期間
- `--cash`：初始資金
- `--short-window`：短均線週期
- `--long-window`：長均線週期
- `--refresh-data`：忽略快取，重新下載資料

## 輸出內容

執行後會在 [outputs](F:\learndata\econamic_reload\outputs) 產生：

- `account.json`：最新帳戶狀態
- `account_summary.csv`：每日帳戶摘要
- `*_equity_curve.csv`：回測資金曲線
- `*_backtest.png`：回測圖表
- `data_cache/`：下載後的歷史資料快取

## 備註

- 此專案偏向學習與模擬用途，不是正式交易系統
- 專案已將原本散落的帳戶與資料輸出集中到 `outputs/`
