import numpy as np


def add_sma_crossover(df):
    copy = df.copy()
    copy["SMA_50"] = copy["Close"].rolling(50).mean()
    copy["SMA_200"] = copy["Close"].rolling(200).mean()
    return copy


def add_bollinger_bands(df):
    copy = df.copy()
    
    sma_20 = copy["Close"].rolling(20)
    mean = sma_20.mean()
    two_sigmas = 2 * sma_20.std()

    copy["SMA_20"] = mean
    copy["UpperBB"] = mean + two_sigmas
    copy["LowerBB"] = mean - two_sigmas
    
    return copy


def add_stochastic_oscillator(df, periods=14):
    copy = df.copy()
    
    high_roll = copy["High"].rolling(periods).max()
    low_roll = copy["Low"].rolling(periods).min()
    
    # Fast stochastic indicator
    num = copy["Close"] - low_roll
    denom = high_roll - low_roll
    copy["%K"] = (num / denom) * 100
    
    # Slow stochastic indicator
    copy["%D"] = copy["%K"].rolling(3).mean()
    
    return copy


# https://www.roelpeters.be/many-ways-to-calculate-the-rsi-in-python-pandas/
def add_rsi(df, periods=14):
    copy = df.copy()
    
    close_diff = copy["Close"].diff()
    up = close_diff.clip(lower=0)
    down = -1 * close_diff.clip(upper=0)

    ma_up = up.ewm(com=periods-1, adjust=True, min_periods=periods).mean()
    ma_down = down.ewm(com=periods-1, adjust=True, min_periods=periods).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    copy["RSI"] = rsi
    
    return copy


def add_macd(df):
    copy = df.copy()
    
    ema_12 = copy["Close"].ewm(span=12, adjust=False, min_periods=12).mean()
    ema_26 = copy["Close"].ewm(span=26, adjust=False, min_periods=26).mean()
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9, adjust=False, min_periods=9).mean()
    diff = macd - signal
    
    copy["MACD"] = macd
    copy["MACD-s"] = signal
    copy["MACD-h"] = diff
    
    return copy


def add_obv(df):
    copy = df.copy()
    # https://stackoverflow.com/a/66827219
    copy["OBV"] = (np.sign(copy["Close"].diff()) * copy["Volume"]).fillna(0).cumsum()
    return copy
