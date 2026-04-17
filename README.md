# Backtesting Project Collection

本倉庫收錄 4 個彼此獨立的 Python 回測與交易模擬專案，內容涵蓋策略回測、均線交易、技術指標實驗，以及以既有資料集重建投資報酬流程。

整合目的如下：

- 保留各專案原本的策略概念與執行方式
- 補齊公開展示所需的文件與專案結構
- 清理不適合公開的本地環境、輸出檔與暫存內容

## 專案列表

### `econamic_model_test`

以追價邏輯為核心的台股回測專案，支援歷史資料取得、策略執行、績效摘要與圖表輸出。

技術基礎：
- Python
- pandas
- matplotlib
- yfinance
- tvDatafeed fallback

### `econamic_reload`

以移動平均交叉概念為主的交易模擬專案，包含資料下載、帳戶更新、資產變化追蹤與結果輸出。

技術基礎：
- Python
- pandas
- FinMind
- matplotlib

### `TB_Strategy`

以技術分析為主軸的回測腳本，涵蓋部位管理、停損、最大回撤與績效統計。

技術基礎：
- Python
- pandas
- matplotlib
- yfinance

### `PY_mod_econamic`

以既有股票資料集為基礎的報酬模擬專案，可比較策略資產曲線與 Buy and Hold 表現。

技術基礎：
- Python
- pandas
- matplotlib
- Excel dataset pipeline

## 執行方式

各資料夾為獨立專案，請分別安裝依賴並執行。

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

公開版整合包已完成以下處理：

- 保留各專案獨立結構，不強行合併為單一框架
- 補齊 README 與基本執行說明
- 排除輸出檔、暫存檔與本地環境
- 清理 `.venv`、`outputs`、快取與帳務相關本地檔案
- 保留必要的輸入資料與可重現的執行入口

## 注意事項

- 本倉庫以學習、研究與作品展示為主，不構成投資建議
- 部分資料來源依賴第三方服務，若服務限制變動，可能需要調整執行方式
- 若需展示最新成果，建議重新執行各專案以產生最新圖表與報表
