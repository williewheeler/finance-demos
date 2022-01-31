import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mplfinance as mpf

from matplotlib.lines import Line2D


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
        title=f"{symbol} Price, {rng}",
        ylabel="Price ($)",
        volume=True,
        ylabel_lower="Volume",
        show_nontrading=False,
        mav=(4),
        figsize=(8, 3),
        style="yahoo",
        datetime_format="%Y-%m-%d")


def plot_sma_crossover(df, symbol, rng):
    start = date_ranges[rng]
    end = today_str
    temp_df = df.loc[start:end, ["Close", "SMA_50", "SMA_200"]]
    temp_df.plot(
        title=f"{symbol} SMA Crossover, {rng}",
        style=["-", "-", "--"],
        figsize=(8, 3))


# TODO Support plotting against index and also peers
def plot_capital_appreciation(df, symbol, rng):
    start = date_ranges[rng]
    end = today_str
    
    # Combined frame with multiple tickers.
    # Currently there's just one but we want to add index and peers as indicated above.
    comb_df = pd.DataFrame({
        symbol: df.loc[start:end, "Close"],
    })
    
    norm_df = comb_df.div(comb_df.iloc[0])
    norm_df.plot(title=f"{symbol} capital appreciation, {rng}", figsize=(8, 3))


def plot_bollinger(df, symbol, rng):
    start = date_ranges[rng]
    end = today_str
    temp_df = df.loc[start:end, ["Close", "SMA_20", "UpperBB", "LowerBB"]]
    temp_df.plot(
        title=f"{symbol} with Bollinger Bands, {rng}",
        style=["-", "--", "-", "-"],
        figsize=(8, 3))


def plot_stochastic_oscillator(df, symbol, rng, periods=14):
    start = date_ranges[rng]
    end = today_str
    temp_df = df[start:end]
    
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, tight_layout=True, figsize=(8, 6))

    ax[0].set_title(f"{symbol} price, {rng}")
    ax[0].plot(temp_df["Close"], color="tab:blue")

    ax[1].set_title(f"{symbol} Stochastic Oscillator ({periods}-day period), {rng}")
    ax[1].set_ylim(-10, 110)
    ax[1].plot(temp_df["%K"], color="tab:blue") # fast
    ax[1].plot(temp_df["%D"], color="tab:orange") # slow
    ax[1].axhline(80, color="tab:red", ls="--")
    ax[1].axhline(20, color="tab:green", ls="--")

    custom_lines = [
        Line2D([0], [0], color="tab:blue", lw=4),
        Line2D([0], [0], color="tab:orange", lw=4),
        Line2D([0], [0], color="tab:red", lw=4),
        Line2D([0], [0], color="tab:green", lw=4),
    ]
    ax[1].legend(custom_lines, ["%K", "%D", "Overbought", "Oversold"], loc="best")


def plot_rsi(df, symbol, rng, periods=14):
    start = date_ranges[rng]
    end = today_str
    temp_df = df[start:end]
    
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, tight_layout=True, figsize=(8, 6))

    ax[0].set_title(f"{symbol} price, {rng}")
    ax[0].plot(temp_df["Close"])

    ax[1].set_title(f"{symbol} RSI ({periods}-day moving average), {rng}")
    ax[1].set_ylim(0, 100)
    ax[1].plot(temp_df["RSI"])
    ax[1].axhline(70, color="tab:red", ls="--")
    ax[1].axhline(30, color="tab:green", ls="--")

    custom_lines = [
        Line2D([0], [0], color="tab:red", lw=4),
        Line2D([0], [0], color="tab:green", lw=4)
    ]
    ax[1].legend(custom_lines, ["Overbought", "Oversold"], loc="best")


def plot_macd(df, symbol, rng, periods=14):
    start = date_ranges[rng]
    end = today_str
    temp_df = df[start:end]
    
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, tight_layout=True, figsize=(8, 6))

    ax[0].set_title(f"{symbol} price, {rng}")
    ax[0].plot(temp_df["Close"])

    ax[1].set_title(f"{symbol} MACD, {rng}")
    ax[1].plot(temp_df["MACD"], color="tab:blue") # slow signal
    ax[1].plot(temp_df["MACD-s"], color="tab:orange") # fast signal
    ax[1].bar(temp_df.index, height=temp_df["MACD-h"], color="black") # diff

    custom_lines = [
        Line2D([0], [0], color="tab:blue", lw=4),
        Line2D([0], [0], color="tab:orange", lw=4),
        Line2D([0], [0], color="black", lw=4)
    ]
    ax[1].legend(custom_lines, ["MACD", "Signal", "Diff"], loc="best")

    
def plot_obv(df, symbol, rng):    
    start = date_ranges[rng]
    end = today_str
    temp_df = df[start:end]
    
    # See
    # https://github.com/matplotlib/mplfinance/blob/master/examples/addplot.ipynb
    # https://github.com/matplotlib/mplfinance/blob/8fa38f2dcd6d3b75c97145b5ded953f13641625e/src/mplfinance/plotting.py#L36
    obv_addplot = mpf.make_addplot(temp_df["OBV"], width=2, panel=2, ylabel="OBV")
    
    # See https://github.com/DanielGoldfarb/mplfinance/blob/master/examples/panels.ipynb
    mpf.plot(
        temp_df,
        addplot=obv_addplot,
        type="candle",
        title=f"{symbol} Price and On-Balance Volume, {rng}",
        ylabel="Price ($)",
        volume=True,
        ylabel_lower="Volume",
        show_nontrading=False,
        style="yahoo",
        figsize=(8, 4),
        panel_ratios=(3, 1, 2),
        datetime_format="%Y-%m-%d")
