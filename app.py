from data_sources.yahoo_finance import YahooFinanceDataSource
from services.data_processor import process_data
import pandas as pd
import warnings

warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")

def main():
    ds = YahooFinanceDataSource()
    raw_df = ds.fetch_data("AAPL", start_date="2025-01-01", end_date="2025-02-28")
    
    processed_df = process_data(raw_df)
    
    print(processed_df)

if __name__ == "__main__":
    main()