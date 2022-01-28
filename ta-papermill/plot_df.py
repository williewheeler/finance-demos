import datetime
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

today = datetime.datetime.now()

date_pattern = "%Y-%m-%d"
today_str = today.strftime(date_pattern)
date_ranges = {
    "1M": (today - datetime.timedelta(days=30)).strftime(date_pattern),
    "3M": (today - datetime.timedelta(days=90)).strftime(date_pattern),
    "6M": (today - datetime.timedelta(days=180)).strftime(date_pattern),
    "1Y": (today - datetime.timedelta(days=365)).strftime(date_pattern),
    "2Y": (today - datetime.timedelta(days=2*365)).strftime(date_pattern),
}


def plot_candlestick(df, symbol, rng):
    start = date_ranges[rng]
    end = today_str
    mpf.plot(
        df[start:end],
        type="candle",
        title=f"{symbol} price, {rng}",
        ylabel="Price ($)",
        volume=True,
        ylabel_lower="Volume",
        show_nontrading=False,
        mav=(4),
        figsize=(8, 4),
        style="yahoo")


# TODO Support plotting against index and also peers
def plot_capital_appreciation(df, symbol, rng):
    start = date_ranges[rng]
    end = today_str
    
    # Combined frame with multiple tickers.
    # Currently there's just one but we want to add index and peers as indicated above.
    comb_df = pd.DataFrame({
        symbol: df[start:end]["Close"],
    })
    
    norm_df = comb_df.div(comb_df.iloc[0])
    norm_df.plot(title=f"{symbol} capital appreciation, {rng}", figsize=(6, 3))


def plot_bollinger(df, symbol, rng):
    start = date_ranges[rng]
    end = today_str
    temp_df = df[start:end][["Close", "SMA_20", "UpperBB", "LowerBB"]]    
    temp_df.plot(
        title=f"{symbol} with Bollinger Bands, {rng}",
        style=["-", "--", "-", "-"],
        figsize=(6, 4))
