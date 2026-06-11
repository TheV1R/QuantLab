from indicators import moving_average, rsi, macd


# =========================
# MOVING AVERAGE STRATEGY
# =========================
def moving_average_strategy(data):

    data['MA50'] = moving_average(data, 50)
    data['MA200'] = moving_average(data, 200)

    data['Signal'] = 0

    # Golden Cross (BUY)
    data.loc[
        (data['MA50'] > data['MA200']) &
        (data['MA50'].shift(1) <= data['MA200'].shift(1)),
        'Signal'
    ] = 1

    # Death Cross (SELL)
    data.loc[
        (data['MA50'] < data['MA200']) &
        (data['MA50'].shift(1) >= data['MA200'].shift(1)),
        'Signal'
    ] = -1

    data['Position'] = data['Signal']

    return data


# =========================
# RSI STRATEGY
# =========================
def rsi_strategy(data):

    data['RSI'] = rsi(data)

    data['Signal'] = 0

    data.loc[data['RSI'] < 30, 'Signal'] = 1
    data.loc[data['RSI'] > 70, 'Signal'] = -1

    data['Position'] = data['Signal'].diff()

    return data


# =========================
# MACD STRATEGY
# =========================
def macd_strategy(data):

    data['MACD'], data['Signal_Line'] = macd(data)

    data['Signal'] = 0

    # Proper crossover logic
    data.loc[
        (data['MACD'] > data['Signal_Line']) &
        (data['MACD'].shift(1) <= data['Signal_Line'].shift(1)),
        'Signal'
    ] = 1

    data.loc[
        (data['MACD'] < data['Signal_Line']) &
        (data['MACD'].shift(1) >= data['Signal_Line'].shift(1)),
        'Signal'
    ] = -1

    data['Position'] = data['Signal']

    return data