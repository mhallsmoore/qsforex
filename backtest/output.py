import os, os.path

import pandas as pd
import matplotlib.pyplot as plt

from qsforex.settings import OUTPUT_RESULTS_DIR


if __name__ == "__main__":
    """
    A simple script to plot the balance of the portfolio, or
    "equity curve", as a function of time.

    It requires OUTPUT_RESULTS_DIR to be set in the project
    settings.
    """
    equity_file = os.path.join(OUTPUT_RESULTS_DIR, "equity.csv")
    equity = pd.io.parsers.read_csv(
        equity_file, header=True, 
        names=["time", "balance"], 
        parse_dates=True, index_col=0
    )
    equity["balance"].plot()
    plt.show()