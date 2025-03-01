import pandas as pd
import yfinance as yf
from .base_source import BaseDataSource

class YahooFinanceDataSource(BaseDataSource):
    """Yahoo Finance data source."""

    def fetch_data(self, symbol: str, start_date: str = None, end_date: str = None, **kwargs) -> pd.DataFrame:
        """Fetch market data for a symbol and return a DataFrame."""
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date)
        return df.sort_index()