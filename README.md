# Backtesting Project Collection

這個倉庫整理了 4 個彼此獨立的 Python 回測與交易模擬專案，保留原本策略概念，同時補齊可交付需要的結構、中文文件與公開前清理。

這份整合包的目標不是把所有策略硬整合成單一框架，而是以作品集的方式呈現不同類型的量化練習：

- 策略回測
- 均線交易模擬
- 技術指標實驗
- 以既有資料集重建投資報酬流程

## 專案列表

### `econamic_model_test`

以追價邏輯為核心的台股回測專案，支援抓取歷史資料、執行策略、輸出績效摘要與圖表。

技術重點：
- Python
- pandas
- matplotlib
- yfinance
- tvDatafeed fallback

### `econamic_reload`

以移動平均交叉概念為主的交易模擬專案，包含資料下載、帳戶更新、資產變化追蹤與輸出結果。

技術重點：
- Python
- pandas
- FinMind
- matplotlib

### `TB_Strategy`

偏向技術分析風格的回測腳本，包含部位管理、停損、最大回撤與績效統計。

技術重點：
- Python
- pandas
- matplotlib
- yfinance

### `PY_mod_econamic`

以既有股票資料集為基礎的報酬模擬專案，可比較策略資產曲線與 Buy and Hold。

技術重點：
- Python
- pandas
- matplotlib
- Excel dataset pipeline

## 快速開始

每個資料夾都是獨立專案，請分別安裝依賴並執行。

### `econamic_model_test`

```bash
cd econamic_model_test
pip install -r requirements.txt
python main.py --symbol 2330 --years 3 --cash 100000
```

### `econamic_reload`

```bash
cd econamic_reload
pip install -r requirements.txt
python main.py --symbol 2330 --years 5
```

### `TB_Strategy`

```bash
cd TB_Strategy
pip install -r requirements.txt
python TB_Strategy.py --symbol 2330 --years 5 --evaluation-years 2
```

### `PY_mod_econamic`

```bash
cd PY_mod_econamic
pip install -r requirements.txt
python return_test.py --dataset google
```

## 倉庫結構

```text
backtesting-project-collection/
├─ econamic_model_test/
├─ econamic_reload/
├─ TB_Strategy/
├─ PY_mod_econamic/
└─ README.md
```

## 整理內容

這份公開版整合包已經做過以下處理：

- 保留各專案獨立結構，不強行合併
- 補齊中文 README 與執行方式
- 將輸出檔與暫存檔排除在版本控制之外
- 清除 `.venv`、`outputs`、快取與本地帳務檔
- 保留必要的輸入資料與可重現執行入口

## 注意事項

- 本倉庫以學習、研究與作品展示為主，不構成投資建議
- 部分資料來源仰賴第三方服務，若服務端限制變動，結果可能需要調整
- 若要進一步展示成果，建議各專案執行後自行產生最新圖表與報表
