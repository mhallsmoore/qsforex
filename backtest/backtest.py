from __future__ import print_function

import copy
try:
    import Queue as queue
except ImportError:
    import queue
import threading
import time
from decimal import Decimal, getcontext

from qsforex.execution.execution import SimulatedExecution
from qsforex.portfolio.portfolio import Portfolio
from qsforex import settings
from qsforex.strategy.strategy import TestStrategy, MovingAverageCrossStrategy
from qsforex.data.price import HistoricCSVPriceHandler


def backtest(
        events, ticker, strategy, portfolio, 
        execution, heartbeat, max_iters=200000
    ):
    """
    Carries out an infinite while loop that polls the 
    events queue and directs each event to either the
    strategy component of the execution handler. The
    loop will then pause for "heartbeat" seconds and
    continue unti the maximum number of iterations is
    exceeded.
    """
    iters = 0
    while True and iters < max_iters:
        ticker.stream_next_tick()
        try:
            event = events.get(False)
        except queue.Empty:
            pass
        else:
            if event is not None:
                if event.type == 'TICK':
                    strategy.calculate_signals(event)
                    portfolio.update_portfolio(event)
                elif event.type == 'SIGNAL':
                    portfolio.execute_signal(event)
                elif event.type == 'ORDER':
                    execution.execute_order(event)
        time.sleep(heartbeat)
        iters += 1
    portfolio.output_results()


if __name__ == "__main__":
    heartbeat = 0.0
    events = queue.Queue()
    equity = settings.EQUITY

    # Load the historic CSV tick data files
    pairs = ["GBPUSD"]
    csv_dir = settings.CSV_DATA_DIR
    if csv_dir is None:
        print("No historic data directory provided - backtest terminating.")
        sys.exit()

    # Create the historic tick data streaming class
    ticker = HistoricCSVPriceHandler(pairs, events, csv_dir)

    # Create the strategy/signal generator, passing the 
    # instrument and the events queue
    strategy = MovingAverageCrossStrategy(
        pairs, events, 500, 2000
    )

    # Create the portfolio object to track trades
    portfolio = Portfolio(
        ticker, events, equity=equity, backtest=True
    )

    # Create the simulated execution handler
    execution = SimulatedExecution()
    
    # Carry out the backtest loop
    backtest(events, ticker, strategy, portfolio, execution, heartbeat)
