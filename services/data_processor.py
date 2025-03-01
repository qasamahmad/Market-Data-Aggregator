import pandas as pd
import numpy as np

def process_data(df):
    """Clean and enrich stock data with technical indicators."""
    # Ensure Date is the index
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)

    # Handle missing data
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    # Use adjusted close if available; otherwise, adjust manually
    if 'Adj Close' in df.columns:
        df['Close'] = df['Adj Close'].copy()
    else:
        if 'Split' in df.columns:
            split_factor = df['Split'][::-1].cumprod()[::-1]
            for col in ['Open', 'High', 'Low', 'Close']:
                if col in df.columns:
                    df[col] = df[col] / split_factor
        if 'Dividend' in df.columns:
            div_cum = df['Dividend'][::-1].cumsum()[::-1]
            for col in ['Open', 'High', 'Low', 'Close']:
                if col in df.columns:
                    df[col] = df[col] + div_cum

    # Normalize close price to a baseline of 1.0
    df['Normalized'] = df['Close'] / df['Close'].iloc[0]

    # Simple Moving Averages (50-day and 200-day)
    df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
    df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()

    # 20-day Exponential Moving Average
    df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()

    # MACD: difference of 12-day and 26-day EMA; signal line is 9-day EMA of MACD
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_hist'] = df['MACD'] - df['MACD_signal']

    # RSI (14-day)
    delta = df['Close'].diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    avg_gain = up.rolling(window=14, min_periods=14).mean()
    avg_loss = down.rolling(window=14, min_periods=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # On-Balance Volume (OBV)
    if 'Volume' in df.columns:
        price_change = df['Close'].diff()
        volume_flow = np.where(price_change > 0, df['Volume'],
                               np.where(price_change < 0, -df['Volume'], 0))
        df['OBV'] = volume_flow.cumsum().astype(float)

    return df