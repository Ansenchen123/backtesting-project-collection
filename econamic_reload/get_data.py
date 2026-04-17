from __future__ import annotations

from dataclasses import dataclass
import datetime as dt
from pathlib import Path

import pandas as pd
from FinMind.data import DataLoader


@dataclass
class DataFetcher:
    years: int = 5
    start_date: dt.date | None = None
    end_date: dt.date | None = None
    cache_dir: Path = Path("data_cache")

    def __post_init__(self) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.api = DataLoader()
        self.df = pd.DataFrame()

    def download_stock_data(self, stock_id: str = "2330", refresh: bool = False) -> pd.DataFrame:
        cache_path = self.cache_dir / f"{stock_id}_data.csv"
        legacy_cache_path = Path(f"{stock_id}_data.csv")
        if cache_path.exists() and not refresh:
            self.df = pd.read_csv(cache_path)
            return self.df
        if legacy_cache_path.exists() and not refresh:
            self.df = pd.read_csv(legacy_cache_path)
            self.df.to_csv(cache_path, index=False)
            return self.df

        start_date = self.start_date or (dt.date.today() - dt.timedelta(days=self.years * 365))
        end_date = self.end_date or dt.date.today()
        self.df = self.api.taiwan_stock_daily(
            stock_id=stock_id,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
        )
        self.df.to_csv(cache_path, index=False)
        return self.df

    def iter_days(self) -> pd.DataFrame:
        if self.df.empty:
            raise ValueError("Call download_stock_data before iterating over data.")
        frame = self.df.copy()
        frame["date"] = pd.to_datetime(frame["date"])
        return frame.sort_values("date").reset_index(drop=True)
