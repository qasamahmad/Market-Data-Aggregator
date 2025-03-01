import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from datetime import date, timedelta
import plotly.graph_objects as go

from services.data_processor import process_data
from services.data_fetcher import fetch_data
from database.db_connection import get_db_connection

@st.cache_data(ttl=600)
def get_data_from_db(symbol, start, end):
    conn = get_db_connection()
    query = f"""
        SELECT date, open, high, low, close, volume, source
        FROM prices
        WHERE symbol = '{symbol}'
          AND date BETWEEN '{start}' AND '{end}'
        ORDER BY date;
    """
    df = pd.read_sql(query, conn, parse_dates=["date"])
    conn.close()
    if not df.empty:
        df.set_index("date", inplace=True)
    return df

# --- Streamlit App Interface ---
st.title("Stock Market Data Dashboard")

# Sidebar controls
st.sidebar.header("Controls")
symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]
symbol = st.sidebar.selectbox("Stock Symbol", symbols)

today = date.today()
default_start = today - timedelta(days=365)
start_date, end_date = st.sidebar.date_input("Date Range", value=(default_start, today))

source_option = st.sidebar.radio(
    "Data Source",
    ["Aggregated (Database)", "Alpha Vantage API", "Yahoo Finance API"]
)

refresh = st.sidebar.button("Refresh Data")

# Optional: moving average control
show_ma = st.sidebar.checkbox("Show Moving Average", value=True)
ma_window = st.sidebar.slider("MA Window (days)", min_value=5, max_value=50, value=20) if show_ma else None

@st.cache_data(ttl=600)
def get_stock_data(symbol, start_date, end_date, source):
    if source == "Aggregated (Database)":
        df = get_data_from_db(symbol, start_date, end_date)
        if not df.empty:
            return df
        else:
            return fetch_data(symbol, start_date=str(start_date), end_date=str(end_date), source="yahoo")
    elif source == "Yahoo Finance API":
        return fetch_data(symbol, start_date=str(start_date), end_date=str(end_date), source="yahoo")
    elif source == "Alpha Vantage API":
        return fetch_data(symbol, start_date=str(start_date), end_date=str(end_date), source="alpha")
    else:
        st.error("Unsupported data source")
        return pd.DataFrame()

if refresh:
    st.cache_data.clear()

raw_df = get_stock_data(symbol, start_date, end_date, source_option)

if raw_df.empty:
    st.warning("No data available for the selected parameters.")
else:
    processed_df = process_data(raw_df)

    # --- Line Chart ---
    st.subheader(f"{symbol} Price Trend")
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=processed_df.index, y=processed_df["close"],
                                  mode='lines', name='Close'))
    if show_ma and "close" in processed_df.columns:
        ma_series = processed_df["close"].rolling(window=ma_window, min_periods=1).mean()
        fig_line.add_trace(go.Scatter(x=processed_df.index, y=ma_series,
                                      mode='lines', name=f"{ma_window}-day MA"))
    fig_line.update_layout(xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig_line, use_container_width=True)

    # --- Candlestick Chart ---
    st.subheader(f"{symbol} Candlestick Chart")
    fig_candle = go.Figure(data=[go.Candlestick(
        x=processed_df.index,
        open=processed_df["open"],
        high=processed_df["high"],
        low=processed_df["low"],
        close=processed_df["close"],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])
    fig_candle.update_layout(xaxis_title="Date", yaxis_title="Price", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig_candle, use_container_width=True)

    # Optionally: Volume chart
    if "volume" in processed_df.columns:
        st.subheader("Volume")
        fig_vol = go.Figure(data=[go.Bar(x=processed_df.index, y=processed_df["volume"], name="Volume")])
        fig_vol.update_layout(xaxis_title="Date", yaxis_title="Volume")
        st.plotly_chart(fig_vol, use_container_width=True)