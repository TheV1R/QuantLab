from strategies import moving_average_strategy, rsi_strategy, macd_strategy
from backtester import backtest
from metrics import total_return, sharpe_ratio, max_drawdown


# =========================
# MULTI-STRATEGY RUNNER
# =========================
def run_strategies(data):

    results = []

    strategies = {
        "MA Crossover": moving_average_strategy,
        "RSI": rsi_strategy,
        "MACD": macd_strategy
    }

    for name, strategy in strategies.items():

        df = data.copy()

        df = strategy(df)
        df = backtest(df)

        results.append({
            "Strategy": name,
            "Return": float(total_return(df)),
            "Sharpe": float(sharpe_ratio(df)),
            "Drawdown": float(max_drawdown(df))
        })

    return results


# =========================
# PARAMETER OPTIMIZATION
# =========================
def optimize_ma(data):

    results = []

    short_windows = [10, 20, 50]
    long_windows = [100, 150, 200]

    for short in short_windows:
        for long in long_windows:

            if short >= long:
                continue

            df = data.copy()

            df['MA_Short'] = df['Close'].rolling(short).mean()
            df['MA_Long'] = df['Close'].rolling(long).mean()

            df['Signal'] = 0
            df.loc[df['MA_Short'] > df['MA_Long'], 'Signal'] = 1
            df.loc[df['MA_Short'] < df['MA_Long'], 'Signal'] = -1

            df['Position'] = df['Signal'].diff()

            df = backtest(df)

            results.append({
                "Short": short,
                "Long": long,
                "Return": float(total_return(df))
            })

    return results
    from strategies import moving_average_strategy, rsi_strategy, macd_strategy
from backtester import backtest
from metrics import total_return, sharpe_ratio, max_drawdown


# =========================
# MULTI-STRATEGY RUNNER
# =========================
def run_strategies(data):

    results = []

    strategies = {
        "MA Crossover": moving_average_strategy,
        "RSI": rsi_strategy,
        "MACD": macd_strategy
    }

    for name, strategy in strategies.items():

        df = data.copy()

        df = strategy(df)
        df = backtest(df)

        results.append({
            "Strategy": name,
            "Return": float(total_return(df)),
            "Sharpe": float(sharpe_ratio(df)),
            "Drawdown": float(max_drawdown(df))
        })

    return results


# =========================
# PARAMETER OPTIMIZATION
# =========================
def optimize_ma(data):

    results = []

    short_windows = [10, 20, 50]
    long_windows = [100, 150, 200]

    for short in short_windows:
        for long in long_windows:

            if short >= long:
                continue

            df = data.copy()

            df['MA_Short'] = df['Close'].rolling(short).mean()
            df['MA_Long'] = df['Close'].rolling(long).mean()

            df['Signal'] = 0
            df.loc[df['MA_Short'] > df['MA_Long'], 'Signal'] = 1
            df.loc[df['MA_Short'] < df['MA_Long'], 'Signal'] = -1

            df['Position'] = df['Signal'].diff()

            df = backtest(df)

            results.append({
                "Short": short,
                "Long": long,
                "Return": float(total_return(df))
            })

    return results

