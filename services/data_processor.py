import pandas as pd
import numpy as np

def process_data(df):
    """Clean and enrich stock data with technical indicators."""
    # Ensure Date is the index
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
    elif 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)
    
    # Standardize column names to lowercase
    df.columns = df.columns.str.lower()
    
    # Fill missing data using forward and backward fill
    df.ffill(inplace=True)
    df.bfill(inplace=True)
    
    # Use adjusted close if available; otherwise, use close (and adjust if needed)
    if 'adj close' in df.columns:
        df['close'] = df['adj close']
    if 'close' not in df.columns:
        raise KeyError("Expected column 'close' not found in data.")
    
    # Normalize close price
    df['normalized'] = df['close'] / df['close'].iloc[0]
    
    # Simple Moving Averages
    df['sma_50'] = df['close'].rolling(window=50, min_periods=1).mean()
    df['sma_200'] = df['close'].rolling(window=200, min_periods=1).mean()
    
    # Exponential Moving Average (20-day)
    df['ema_20'] = df['close'].ewm(span=20, adjust=False).mean()
    
    # MACD
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['macd_hist'] = df['macd'] - df['macd_signal']
    
    # RSI (14-day)
    delta = df['close'].diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    avg_gain = up.rolling(window=14, min_periods=14).mean()
    avg_loss = down.rolling(window=14, min_periods=14).mean()
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # On-Balance Volume (OBV)
    if 'volume' in df.columns:
        price_change = df['close'].diff()
        volume_flow = np.where(price_change > 0, df['volume'],
                               np.where(price_change < 0, -df['volume'], 0))
        df['obv'] = volume_flow.cumsum().astype(float)
    
    return df