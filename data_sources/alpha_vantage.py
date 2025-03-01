import os
import requests
import pandas as pd
from dotenv import load_dotenv
from .base_source import BaseDataSource

load_dotenv()

class AlphaVantageDataSource(BaseDataSource):
    """Alpha Vantage data source."""

    def fetch_data(self, symbol: str, start_date: str = None, end_date: str = None, **kwargs) -> pd.DataFrame:
        """Fetch daily market data for a symbol."""
        api_key = os.getenv("ALPHAVANTAGE_API_KEY")
        if not api_key:
            raise ValueError("ALPHAVANTAGE_API_KEY not set")
        
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": api_key,
            "outputsize": kwargs.get("outputsize", "compact"),
            "datatype": kwargs.get("datatype", "json")
        }
        response = requests.get(url, params=params)
        data = response.json()
        ts = data.get("Time Series (Daily)")
        if not ts:
            return pd.DataFrame()
        
        df = pd.DataFrame.from_dict(ts, orient="index")
        df.index = pd.to_datetime(df.index)
        df = df.rename(columns={
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. volume": "volume"
        }).apply(pd.to_numeric)
        
        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]
        
        return df.sort_index()