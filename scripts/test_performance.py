"""
This is a small helper script written to help debug issues
with performance calculation, that avoids having to re-run
the full backtest.

In this case it simply works off the "backtest.csv" file that
is produced from a backtest.py run.
"""


import os

import pandas as pd

from qsforex.performance.performance import create_drawdowns
from qsforex.settings import OUTPUT_RESULTS_DIR


if __name__ == "__main__":
    in_filename = "backtest.csv"
    out_filename = "equity.csv"
    in_file = os.path.join(OUTPUT_RESULTS_DIR, in_filename)
    out_file = os.path.join(OUTPUT_RESULTS_DIR, out_filename)

    # Create equity curve dataframe
    df = pd.read_csv(in_file, index_col=0)
    df.dropna(inplace=True)
    df["Total"] = df.sum(axis=1)
    df["Returns"] = df["Total"].pct_change()
    df["Equity"] = (1.0 + df["Returns"]).cumprod()

    # Create drawdown statistics
    drawdown, max_dd, dd_duration = create_drawdowns(df["Equity"])
    df["Drawdown"] = drawdown
    df.to_csv(out_file, index=True)
