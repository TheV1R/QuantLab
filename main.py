from data_loader import load_data
from strategies import moving_average_strategy
from backtester import backtest

from metrics import (
    total_return,
    sharpe_ratio,
    max_drawdown,
    win_rate,
    volatility,
    profit_factor
)

from research import run_strategies, optimize_ma

import pandas as pd


# =========================
# USER INPUT
# =========================
ticker = input("Enter Stock (e.g., AAPL, TSLA, MSFT): ")
capital = float(input("Enter Initial Capital (e.g., 10000): "))

start_date = "2020-01-01"
end_date = "2025-01-01"

print(f"\nRunning Backtest for {ticker}")
print(f"Initial Capital: {capital}")
print(f"Period: {start_date} to {end_date}")


# =========================
# STEP 1: LOAD DATA
# =========================
data = load_data(ticker, start_date, end_date)


# =========================
# STEP 2: APPLY STRATEGY
# =========================
data = moving_average_strategy(data)


# =========================
# STEP 3: BACKTEST
# =========================
data = backtest(data, initial_capital=capital)


# =========================
# STEP 4: METRICS
# =========================
print("\n===== PERFORMANCE METRICS =====")

print("Total Return:", total_return(data), "%")
print("Sharpe Ratio:", sharpe_ratio(data))
print("Max Drawdown:", max_drawdown(data), "%")
print("Win Rate:", win_rate(data), "%")
print("Volatility:", volatility(data), "%")
print("Profit Factor:", profit_factor(data))


# =========================
# STRATEGY LEADERBOARD
# =========================
results = run_strategies(data)
df_results = pd.DataFrame(results)

print("\n===== STRATEGY LEADERBOARD =====")
print(df_results)


# =========================
# PARAMETER OPTIMIZATION
# =========================
opt_results = optimize_ma(data)
df_opt = pd.DataFrame(opt_results)

print("\n===== PARAMETER OPTIMIZATION (TOP RESULTS) =====")
print(df_opt.sort_values(by="Return", ascending=False).head())


#