import copy
import Queue
import threading
import time
import sys
import logging
from decimal import Decimal, getcontext

from qsforex.execution.execution import SimulatedExecution
from qsforex.portfolio.portfolio import Portfolio
from qsforex import settings
from qsforex.strategy.strategy import TestStrategy
from qsforex.data.price import HistoricCSVPriceHandler

logger = logging.getLogger('main_logger')

def trade(events, strategy, portfolio, execution, heartbeat):
    """
    Carries out an infinite while loop that polls the 
    events queue and directs each event to either the
    strategy component of the execution handler. The
    loop will then pause for "heartbeat" seconds and
    continue.
    """
    while True:
        try:
            event = events.get(False)
        except Queue.Empty:
            pass
        else:
            if event is not None:
                if event.type == 'TICK':
                    strategy.calculate_signals(event)
                elif event.type == 'SIGNAL':
                    portfolio.execute_signal(event)
                    logger.debug(event)
                elif event.type == 'ORDER':
                    execution.execute_order(event)
                    logger.debug(event)
                elif event.type == 'BACKTEST_ENDED':
                    logger.debug("Backtest has ended normally")
                    sys.exit(0)
        time.sleep(heartbeat)


if __name__ == "__main__":
    # Set the number of decimal places to 2
    getcontext().prec = 2

    heartbeat = 0.0  # Half a second between polling
    events = Queue.Queue()
    equity = settings.EQUITY

    # Load the historic CSV tick data files
    pairs = ["GBPUSD"]
    csv_dir = settings.CSV_DATA_DIR
    if csv_dir is None:
        print "No historic data directory provided - backtest terminating."
        sys.exit()

    # Create the historic tick data streaming class
    prices = HistoricCSVPriceHandler(pairs, events, csv_dir)

    # Create the strategy/signal generator, passing the 
    # instrument and the events queue
    strategy = TestStrategy(pairs[0], events)

    # Create the portfolio object to track trades
    portfolio = Portfolio(prices, events, equity=equity)

    # Create the simulated execution handler
    execution = SimulatedExecution()
    
    # Create two separate threads: One for the trading loop
    # and another for the market price streaming class
    trade_thread = threading.Thread(
        target=trade, args=(
            events, strategy, portfolio, execution, heartbeat
        )
    )
    price_thread = threading.Thread(target=prices.stream_to_queue, args=[])
    
    # Start both threads
    trade_thread.start()
    price_thread.start()