# econamic_model_test

本專案為台股追價策略回測實驗，重點在於以歷史股價資料模擬策略進出場，並輸出資產曲線、交易紀錄與績效摘要。

## 功能內容

- 下載或讀取指定股票的歷史價格資料
- 依追價邏輯計算進出場訊號
- 輸出回測摘要與交易紀錄
- 產生視覺化績效圖表

## 技術基礎

- Python
- pandas
- matplotlib
- yfinance
- tvDatafeed fallback

## 執行方式

```bash
pip install -r requirements.txt
python main.py --symbol 2330 --years 3 --cash 100000
```

常用參數：

- `--symbol`：股票代號
- `--years`：回測年數
- `--cash`：初始資金

## 輸出內容

執行完成後，結果會輸出至 `outputs/`，包含：

- 回測摘要
- 交易紀錄
- 資產曲線與績效圖表

## 專案結構

```text
econamic_model_test/
├─ main.py
├─ ChasePrice_StF.py
├─ requirements.txt
├─ README.md
└─ tvdatafeed-main/
```

## 注意事項

- 本專案以策略研究與作品展示為主，不構成投資建議
- 若第三方資料來源限制變動，可能需要調整資料取得方式
