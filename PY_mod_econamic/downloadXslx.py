from tvDatafeed import TvDatafeed, Interval
print("a")
import pandas as pd
from datetime import datetime

symbol = "GOOGL"
exchange = "NASDAQ"
interval = Interval.in_daily
estimated_days = 365 * 20  # 抓夠長時間後再過濾

try:
    tv = TvDatafeed()

    print(f"正在下載 股票代碼 {symbol} ...")
    df = tv.get_hist(symbol=symbol, exchange=exchange, n_bars=estimated_days, interval=interval)

    # 處理 DataFrame
    df.index = pd.to_datetime(df.index)
    df.index.name = "Date"
    df = df[["open", "high", "low", "close"]].rename(
        columns={"open": "Open", "high": "High", "low": "Low", "close": "Close"}
    )

    # 過濾出使用者要求的開始時間之後的資料
    df.index = df.index.normalize()
    print(df)

except Exception as e:
    print(f"Error: {e}")
# 儲存資料到 Excel 檔案
output_file = 'google_filtered_data.xlsx'
df.to_excel(output_file)