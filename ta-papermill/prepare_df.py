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
