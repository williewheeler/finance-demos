import os
import papermill as pm

ticker_symbols = [
    "AAPL",
    "AMZN",
    "ARKK",
    "BTC-USD",
    "ETH-USD",
    "EXPE",
    "FB",
    "GOOG",
    "IAU",
    "MSFT",
    "O",
    "PLTR",
    "SBUX",
    "TSLA",
]

out_dir = "./out"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

for ts in ticker_symbols:
    input = "ta.ipynb"
    output = f"{out_dir}/ta-{ts}.ipynb"
    pm.execute_notebook(input, output, parameters={ "ticker_symbol": ts })
