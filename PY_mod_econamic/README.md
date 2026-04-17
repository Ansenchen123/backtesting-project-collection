# PY_mod_econamic

本專案以既有股票資料集為基礎，重建投資報酬模擬流程，並提供策略資產變化與 Buy and Hold 的比較結果。

## 功能內容

- 讀取既有 Excel 資料集
- 依策略條件模擬交易過程
- 計算資產變化與績效表現
- 輸出圖表與比較結果

## 技術基礎

- Python
- pandas
- matplotlib
- Excel dataset pipeline

## 執行方式

```bash
pip install -r requirements.txt
python return_test.py --dataset google
```

可選資料集：

- `google`
- `intel`

## 輸出內容

執行完成後，結果會輸出至 `outputs/`，包含：

- 策略資產曲線圖
- 績效比較圖表
- 模擬結果資料

## 專案結構

```text
PY_mod_econamic/
├─ return_test.py
├─ requirements.txt
├─ google.xlsx
├─ intel.xlsx
└─ README.md
```

## 注意事項

- 本專案以研究與展示用途為主，不構成投資建議
- 若更換資料集格式，請同步調整資料欄位與讀取邏輯
