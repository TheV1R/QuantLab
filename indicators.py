import numpy as np


# =========================
# MOVING AVERAGE
# =========================
def moving_average(data, window):
    return data['Close'].rolling(window=window, min_periods=1).mean()


# =========================
# RSI (Relative Strength Index)
# =========================
def rsi(data, period=14):

    delta = data['Close'].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    # Avoid division by zero
    rs = avg_gain / (avg_loss + 1e-10)

    rsi = 100 - (100 / (1 + rs))

    return rsi


# =========================
# MACD
# =========================
def macd(data):

    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()

    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=9, adjust=False).mean()

    return macd_line, signal_line