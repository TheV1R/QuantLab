import numpy as np


# =========================
# TOTAL RETURN
# =========================
def total_return(data):
    ret = (data['Portfolio'].iloc[-1] / data['Portfolio'].iloc[0]) - 1
    return round(ret * 100, 2)  # percentage


# =========================
# SHARPE RATIO
# =========================
def sharpe_ratio(data):

    returns = data['Portfolio'].pct_change().dropna()

    if returns.std() == 0:
        return 0

    sharpe = np.sqrt(252) * returns.mean() / returns.std()

    return round(sharpe, 2)


# =========================
# MAX DRAWDOWN
# =========================
def max_drawdown(data):

    cumulative = data['Portfolio']
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak

    return round(drawdown.min() * 100, 2)  # percentage


# =========================
# WIN RATE
# =========================
def win_rate(data):

    returns = data['Portfolio'].pct_change().dropna()

    wins = (returns > 0).sum()
    total = len(returns)

    if total == 0:
        return 0

    return round((wins / total) * 100, 2)


# =========================
# VOLATILITY (ANNUALIZED)
# =========================
def volatility(data):

    returns = data['Portfolio'].pct_change().dropna()

    vol = returns.std() * np.sqrt(252)

    return round(vol * 100, 2)  # percentage


# =========================
# PROFIT FACTOR
# =========================
def profit_factor(data):

    returns = data['Portfolio'].pct_change().dropna()

    gains = returns[returns > 0].sum()
    losses = -returns[returns < 0].sum()

    if losses == 0:
        return np.inf

    return round(gains / losses, 2)
    