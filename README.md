# Market Data Aggregator

Market Data Aggregator is a Python-based pipeline that consolidates stock market data from multiple sources, caches it in a PostgreSQL database, processes it by computing technical indicators (such as SMA, EMA, MACD, RSI, OBV, etc.), and displays an interactive dashboard using Streamlit.

## Demo

![Market Data Aggregator Demo](demo.gif)

## Features

- **Multiple Data Sources:** Fetch raw market data from Alpha Vantage and Yahoo Finance.
- **Database Caching:** Store and cache data in PostgreSQL to reduce API calls.
- **Data Processing:** Handle missing values and compute key technical indicators.
- **Interactive Dashboard:** Streamlit front-end with controls and interactive charts.
- **Utilities:** Built-in logging and rate limiting.

## Project Structure

```
Market-Data-Aggregator/
├── LICENSE
├── venv/
├── data_sources/
│   ├── __init__.py
│   ├── base_source.py
│   ├── alpha_vantage.py
│   └── yahoo_finance.py
├── database/
│   ├── __init__.py
│   ├── db_connection.py
│   └── models.py
├── utils/
│   ├── __init__.py
│   ├── rate_limiter.py
│   └── logger.py
├── services/
│   ├── __init__.py
│   ├── data_fetcher.py
│   └── data_processor.py
├── streamlit_app/
│   └── dashboard.py
├── app.py
└── requirements.txt
```

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/Market-Data-Aggregator.git
   cd Market-Data-Aggregator
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Environment Variables:**  
   Create a `.env` file in the project root with your API keys and database URL:

   ```plaintext
   ALPHAVANTAGE_API_KEY=your_alpha_vantage_api_key
   DATABASE_URL=postgresql://username:password@localhost:5432/market_data
   ```

2. **Database Setup:**  
   Ensure PostgreSQL is running and create necessary tables:

   ```bash
   python -m database.models
   ```

## Running the App

### Command-line Demo

Run the script to fetch and process stock data:

```bash
python app.py
```

### Streamlit Dashboard

Launch the interactive dashboard:

```bash
streamlit run streamlit_app/dashboard.py
```

Use the sidebar to select a stock symbol, date range, and data source. Data is retrieved from the database if available; otherwise, it falls back to API requests.

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.