# TB_Strategy

本專案為技術分析導向的回測腳本，涵蓋部位管理、停損控制、最大回撤與績效統計，適合用於觀察單一策略在歷史資料中的表現。

## 功能內容

- 讀取歷史股價資料
- 計算策略條件與進出場邏輯
- 模擬部位與資產變化
- 統計報酬率、最大回撤與交易次數

## 技術基礎

- Python
- pandas
- matplotlib
- yfinance

## 執行方式

```bash
pip install -r requirements.txt
python TB_Strategy.py --symbol 2330 --years 5 --evaluation-years 2
```

常用參數：

- `--symbol`：股票代號
- `--years`：資料年數
- `--evaluation-years`：評估區間
- `--cash`：初始資金
- `--stoploss-pct`：停損百分比

## 輸出內容

執行完成後，結果會輸出至 `outputs/`，包含：

- 回測摘要
- 資產曲線圖
- 交易統計資訊

## 專案結構

```text
TB_Strategy/
├─ TB_Strategy.py
├─ requirements.txt
└─ README.md
```

## 注意事項

- 本專案以策略研究與作品展示為主，不構成投資建議
- 回測結果受資料品質與參數設定影響，使用前建議自行調整驗證
