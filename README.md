# 回測專案整合包

本資料夾收錄了 4 個彼此分離、但都與回測或交易模擬相關的 Python 專案。

這份整合包的目的，是把原本分散的專案集中到同一個資料夾中，方便查看、交付與後續整理；它**不是**要把這 4 個專案合併成同一套系統。

## 收錄專案

### 1. `econamic_model_test`
路徑：[econamic_model_test](F:\learndata\回測專案整合包\econamic_model_test)

簡介：
以台股為主的簡易回測專案，核心是追價策略，會輸出歷史資料、交易紀錄、資金曲線與圖表。

重點：
- 有獨立的策略檔與命令列入口
- 可直接輸出 CSV 與圖表
- 已補上資料來源 fallback，降低執行環境限制

### 2. `econamic_reload`
路徑：[econamic_reload](F:\learndata\回測專案整合包\econamic_reload)

簡介：
以短長均線交叉為基礎的台股模擬交易專案，保留帳戶、交割與每日結算概念。

重點：
- 有資料下載、快取、帳戶管理與回測輸出
- 輸出已集中到 `outputs/`
- 適合展示較完整的模擬交易流程

### 3. `TB_Strategy`
路徑：[TB_Strategy](F:\learndata\回測專案整合包\TB_Strategy)

簡介：
偏趨勢追蹤的回測腳本，包含加碼、停損與最大回撤計算。

重點：
- 有完整策略參數入口
- 會輸出交易紀錄、績效摘要與權益曲線
- 保留原本策略概念，但已整理成較穩定的可執行腳本

### 4. `PY_mod_econamic`
路徑：[PY_mod_econamic](F:\learndata\回測專案整合包\PY_mod_econamic)

簡介：
以 Excel 訊號資料驅動的交易模擬專案，適合驗證外部訊號或分類結果。

重點：
- 使用既有訊號檔與價格檔進行模擬
- 可比較策略結果與 Buy and Hold
- 輸出已集中到 `outputs/`

## 快速操作說明

建議先進入想執行的專案資料夾，再安裝該專案自己的相依套件。

### `econamic_model_test`

```bash
cd econamic_model_test
pip install -r requirements.txt
python main.py
```

自訂參數範例：

```bash
python main.py --symbol 2330 --years 3 --cash 100000
```

### `econamic_reload`

```bash
cd econamic_reload
pip install -r requirements.txt
python main.py
```

自訂參數範例：

```bash
python main.py --symbol 2330 --years 8 --cash 1500000 --short-window 10 --long-window 30
```

### `TB_Strategy`

```bash
cd TB_Strategy
pip install -r requirements.txt
python TB_Strategy.py
```

自訂參數範例：

```bash
python TB_Strategy.py --symbol 2330 --years 10 --cash 1500000 --stoploss-pct 5
```

### `PY_mod_econamic`

```bash
cd PY_mod_econamic
pip install -r requirements.txt
python return_test.py --dataset google
```

切換資料集範例：

```bash
python return_test.py --dataset intel
```

## 整理原則

這份整合包遵守以下原則：

- 維持各專案分離，不強行整合成同一套架構
- 不改變原本策略概念，只修補可交付性與可執行性
- 補齊中文 README、依賴說明與輸出目錄整理
- 保留每個專案自己的執行方式與定位

## 公開前注意事項

各專案都已補上 `.gitignore`，用來排除不適合公開的內容，例如：

- 虛擬環境
- Python 快取檔
- 回測輸出結果
- 本地快取資料
- 根目錄殘留的帳戶摘要、交易紀錄、壓縮檔或臨時資料

如果之後要公開，建議從這份整合包內的專案副本開始整理，而不要直接動原始資料夾。

## 備註

- 原始專案仍保留在 `F:\learndata`，這份資料夾是另外複製出來的整理版本
- 若之後需要進一步打包、壓縮或補交付文件，可以直接在這份整合包上繼續處理
