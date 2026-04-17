# econamic_reload

本專案為移動平均交叉概念的交易模擬實驗，重點在於以歷史資料重建資產變化流程，觀察策略在不同條件下的表現。

## 功能內容

- 下載指定股票的歷史資料
- 計算均線與交易訊號
- 模擬持倉、現金與總資產變化
- 輸出回測摘要與圖表結果

## 技術基礎

- Python
- pandas
- FinMind
- matplotlib

## 執行方式

```bash
pip install -r requirements.txt
python main.py --symbol 2330 --years 5
```

常用參數：

- `--symbol`：股票代號
- `--years`：回測年數
- `--cash`：初始資金
- `--short-window`：短期均線窗口
- `--long-window`：長期均線窗口

## 輸出內容

執行完成後，結果會輸出至 `outputs/`，包含：

- 回測結果摘要
- 資產曲線圖
- 交易過程相關資料

## 專案結構

```text
econamic_reload/
├─ main.py
├─ func.py
├─ get_data.py
├─ requirements.txt
└─ README.md
```

## 注意事項

- 本專案以研究與展示為主，不構成投資建議
- 資料來源仰賴第三方服務，執行前請確認網路與資料服務可用
