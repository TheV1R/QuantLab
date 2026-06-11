import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data_loader import load_data
from strategies import moving_average_strategy, rsi_strategy, macd_strategy
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


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Quant Dashboard", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse at 50% -10%, rgba(255,215,0,0.25), transparent 60%),
        radial-gradient(circle at 90% 10%, rgba(255,215,0,0.08), transparent 50%),
        radial-gradient(circle at 10% 20%, rgba(255,215,0,0.06), transparent 50%),
        #020617;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
div[data-testid="stMetric"] {
    transition: all 0.3s ease;
}

div[data-testid="stMetric"]:hover {
    box-shadow: 0 0 20px rgba(255,215,0,0.4);
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)
st.title("Quant Strategy Research & Backtesting System")
st.markdown("Backtest and analyze trading strategies interactively")

# =========================
# SIDEBAR INPUT
# =========================
st.sidebar.header("⚙️ Settings")

ticker = st.sidebar.text_input("Stock", "AAPL")
capital = st.sidebar.number_input("Initial Capital", value=10000)

strategy_choice = st.sidebar.selectbox(
    "Strategy",
    ["Moving Average", "RSI", "MACD"]
)
# =========================
# TRADING COST SETTINGS
# =========================
cost = st.sidebar.slider("Transaction Cost (%)", 0.0, 1.0, 0.1) / 100
slippage = st.sidebar.slider("Slippage (%)", 0.0, 1.0, 0.05) / 100

run = st.sidebar.button("Run Backtest")

# =========================
# MAIN LOGIC
# =========================
if run:

    data = load_data(ticker, "2020-01-01", "2025-01-01")

    # Apply strategy
    if strategy_choice == "Moving Average":
        data = moving_average_strategy(data)
    elif strategy_choice == "RSI":
        data = rsi_strategy(data)
    elif strategy_choice == "MACD":
        data = macd_strategy(data)

    data = backtest(
    data,
    initial_capital=capital,
    cost=cost,
    slippage=slippage)


    # =========================
    # KPI METRICS (TOP CARDS)
    # =========================
    st.subheader("📈 Performance Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Return (%)", total_return(data))
    col2.metric("Sharpe", sharpe_ratio(data))
    col3.metric("Drawdown (%)", max_drawdown(data))
    col4.metric("Win Rate (%)", win_rate(data))

    col5, col6 = st.columns(2)
    col5.metric("Volatility (%)", volatility(data))
    col6.metric("Profit Factor", profit_factor(data))

    # =========================
    # PRICE + SIGNALS
    # =========================
    st.subheader("📊 Price & Trade Signals")

    fig, ax = plt.subplots(figsize=(12,5))

    ax.plot(data['Close'], label="Price")

    if 'MA50' in data.columns:
        ax.plot(data['MA50'], label="MA50")
        ax.plot(data['MA200'], label="MA200")

    ax.scatter(data.index[data['Position'] == 1],
               data['Close'][data['Position'] == 1],
               marker='^', label='BUY')

    ax.scatter(data.index[data['Position'] == -1],
               data['Close'][data['Position'] == -1],
               marker='v', label='SELL')

    ax.legend()
    st.pyplot(fig)

    # =========================
    # PORTFOLIO CURVE
    # =========================
    st.subheader(" Portfolio Growth")

    fig2, ax2 = plt.subplots(figsize=(12,5))
    ax2.plot(data['Portfolio'])
    ax2.set_title("Portfolio Value")

    st.pyplot(fig2)

    # =========================
    # STRATEGY COMPARISON
    # =========================
    st.subheader(" Strategy Comparison")

    results = run_strategies(data)
    df_results = pd.DataFrame(results)

    st.dataframe(df_results)

    fig3, ax3 = plt.subplots()
    ax3.bar(df_results['Strategy'], df_results['Return'])
    ax3.set_title("Returns Comparison")

    st.pyplot(fig3)

    # =========================
    # HEATMAP
    # =========================
    st.subheader(" MA Optimization Heatmap")

    opt_results = optimize_ma(data)
    df_opt = pd.DataFrame(opt_results)

    heatmap = df_opt.pivot(index="Short", columns="Long", values="Return")

    fig4, ax4 = plt.subplots()
    im = ax4.imshow(heatmap, aspect='auto')

    ax4.set_xticks(range(len(heatmap.columns)))
    ax4.set_yticks(range(len(heatmap.index)))

    ax4.set_xticklabels(heatmap.columns)
    ax4.set_yticklabels(heatmap.index)

    plt.colorbar(im)

    st.pyplot(fig4)

    # =========================
    # DOWNLOAD RESULTS
    # =========================
    st.subheader("⬇️ Download Results")

    csv = df_results.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download Strategy Results CSV",
        data=csv,
        file_name=f"{ticker}_results.csv",
        mime='text/csv'
    )