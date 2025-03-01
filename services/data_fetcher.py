import pandas as pd
from data_sources.alpha_vantage import AlphaVantageDataSource
from data_sources.yahoo_finance import YahooFinanceDataSource

def fetch_data(symbol: str, start_date: str = None, end_date: str = None, source: str = "alpha") -> pd.DataFrame:
    """Fetch data from the selected data source."""
    if source == "alpha":
        ds = AlphaVantageDataSource()
    elif source == "yahoo":
        ds = YahooFinanceDataSource()
    else:
        raise ValueError("Unsupported data source")
    return ds.fetch_data(symbol, start_date, end_date)