def add_bollinger_bands(df):
    copy = df.copy()
    
    sma_20 = copy["Close"].rolling(20)
    mean = sma_20.mean()
    two_sigmas = 2 * sma_20.std()

    copy["SMA_20"] = mean
    copy["UpperBB"] = mean + two_sigmas
    copy["LowerBB"] = mean - two_sigmas
    
    return copy
