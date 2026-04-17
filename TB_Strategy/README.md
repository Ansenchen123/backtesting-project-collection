# TB_Strategy

`TB_Strategy` 是一個趨勢型回測腳本，保留了加碼、停損與最大回撤等交易管理概念。

## 專案內容

- [TB_Strategy.py](F:\learndata\TB_Strategy\TB_Strategy.py)：策略主程式
- `outputs/`：交易紀錄、摘要報表與權益曲線

## 策略說明

此策略以 20 日與 60 日均線為基礎，並加入部位管理：

- 20MA 上穿 60MA 時進場
- 價格延續上漲時可以加碼
- 均線反轉或跌破停損條件時出場

除了最終報酬外，腳本也會輸出交易明細與最大回撤，方便進一步分析。

## 安裝需求

安裝相依套件：

```bash
pip install -r requirements.txt
```

## 執行方式

使用預設參數：

```bash
python TB_Strategy.py
```

自訂回測參數：

```bash
python TB_Strategy.py --symbol 2330 --years 10 --cash 1500000 --stoploss-pct 5
```

可用參數：

- `--symbol`：股票代號
- `--exchange`：交易所，預設 `TWSE`
- `--years`：抓取資料年數
- `--cash`：初始資金
- `--evaluation-years`：實際評估期間
- `--initial-shares-pct`：首次進場資金比例
- `--add-shares-multiplier`：加碼倍率
- `--stoploss-pct`：停損百分比

## 輸出內容

執行後會在 [outputs](F:\learndata\TB_Strategy\outputs) 產生：

- `*_transactions.csv`：交易紀錄
- `*_summary.csv`：績效摘要
- `*_equity_curve.png`：權益曲線圖

## 備註

- 專案優先使用 `tvDatafeed`，若環境缺少相依套件，會自動退回 `yfinance`
- 目前定位為策略驗證腳本，而不是完整交易平台
