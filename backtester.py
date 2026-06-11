def backtest(data, initial_capital=10000, cost=0.001, slippage=0.0005):

    cash = initial_capital
    shares = 0
    portfolio_values = []

    position = 0  # 0 = no position, 1 = holding

    for i in range(len(data)):

        price = float(data['Close'].iloc[i])
        signal = data['Position'].iloc[i]

        # =========================
        # BUY
        # =========================
        if signal == 1 and position == 0:

            # Apply slippage (buy at higher price)
            execution_price = price * (1 + slippage)

            # Apply cost
            shares = (cash * (1 - cost)) / execution_price

            cash = 0
            position = 1

        # =========================
        # SELL
        # =========================
        elif signal == -1 and position == 1:

            # Apply slippage (sell at lower price)
            execution_price = price * (1 - slippage)

            # Apply cost
            cash = shares * execution_price * (1 - cost)

            shares = 0
            position = 0

        # =========================
        # PORTFOLIO VALUE
        # =========================
        portfolio_value = cash + shares * price
        portfolio_values.append(portfolio_value)

    data['Portfolio'] = portfolio_values

    return data