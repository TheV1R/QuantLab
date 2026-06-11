import yfinance as yf
import pandas as pd

def load_data(ticker, start, end):

    print(f"\nDownloading data for {ticker}...")

    data = yf.download(ticker, start=start, end=end, auto_adjust=True)

    # =========================
    # FIX 1: Handle empty data
    # =========================
    if data.empty:
        raise ValueError(f"No data found for {ticker}. Please check the ticker symbol.")

    # =========================
    # FIX 2: Flatten multi-index columns
    # =========================
    if hasattr(data.columns, 'levels'):
        data.columns = data.columns.get_level_values(0)

    # =========================
    # FIX 3: Ensure required columns exist
    # =========================
    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']

    for col in required_cols:
        if col not in data.columns:
            raise ValueError(f"Missing column: {col} in data")

    data = data[required_cols]

    # =========================
    # FIX 4: Convert to numeric 
    # =========================
    data = data.apply(pd.to_numeric, errors='coerce')

    # =========================
    # FIX 5: Drop NaN values
    # =========================
    data.dropna(inplace=True)

    # =========================
    # FIX 6: Sort index 
    # =========================
    data.sort_index(inplace=True)

    print(f"Data Loaded: {len(data)} rows")

    return data