# PY_mod_econamic

`PY_mod_econamic` 是一個以 Excel 訊號檔驅動的交易模擬專案，目的是比較策略資產曲線與單純持有的差異。

## 專案內容

- [return_test.py](F:\learndata\PY_mod_econamic\return_test.py)：模擬交易主程式
- `google.xlsx`、`intel.xlsx`：策略訊號資料
- `google_filtered_data.xlsx`、`intel_filtered_data.xlsx`：價格資料
- `outputs/`：交易紀錄、摘要與模擬圖表

## 模擬邏輯

此專案不是直接從市場資料即時計算訊號，而是：

- 讀取外部整理好的價格資料與訊號資料
- 根據訊號決定持有、買進或出場
- 記錄總資產變化
- 與 Buy and Hold 結果進行比較

因此它比較像「策略訊號驗證工具」，而不是從零產生訊號的完整回測框架。

## 安裝需求

安裝方式：

```bash
pip install -r requirements.txt
```

## 執行方式

執行 Google 範例：

```bash
python return_test.py --dataset google
```

執行 Intel 範例：

```bash
python return_test.py --dataset intel
```

可用參數：

- `--dataset`：`google` 或 `intel`
- `--start-date`：模擬起始日期
- `--cash`：初始資金
- `--fee-rate`：交易成本比率
- `--putcash-mode`：每次投入資金倍率

## 輸出內容

執行後會在 [outputs](F:\learndata\PY_mod_econamic\outputs) 產生：

- `*_trading_log.csv`：每日模擬結果
- `*_summary.csv`：摘要指標
- `*_simulation.png`：策略與持有比較圖

## 備註

- 這個專案的重點是驗證既有訊號資料，而不是建立資料下載流程
- 原本輸出在根目錄的檔案已整理到 `outputs/`
