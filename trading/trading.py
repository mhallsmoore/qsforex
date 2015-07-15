import copy
from decimal import Decimal, getcontext
import logging
import logging.config
try:
    import Queue as queue
except ImportError:
    import queue
import threading
import time

from qsforex.execution.execution import OANDAExecutionHandler
from qsforex.portfolio.portfolio import Portfolio
from qsforex import settings
from qsforex.strategy.strategy import TestStrategy
from qsforex.data.streaming import StreamingForexPrices


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
        except queue.Empty:
            pass
        else:
            if event is not None:
                if event.type == 'TICK':
                    logger.info("Received new tick event: %s", event)
                    strategy.calculate_signals(event)
                    portfolio.update_portfolio(event)
                elif event.type == 'SIGNAL':
                    logger.info("Received new signal event: %s", event)
                    portfolio.execute_signal(event)
                elif event.type == 'ORDER':
                    logger.info("Received new order event: %s", event)
                    execution.execute_order(event)
        time.sleep(heartbeat)


if __name__ == "__main__":
    # Set up logging
    logging.config.fileConfig('../logging.conf')
    logger = logging.getLogger('qsforex.trading.trading')

    # Set the number of decimal places to 2
    getcontext().prec = 2

    heartbeat = 0.0  # Time in seconds between polling
    events = queue.Queue()
    equity = settings.EQUITY

    # Pairs to include in streaming data set
    pairs = ["EURUSD", "GBPUSD"]

    # Create the OANDA market price streaming class
    # making sure to provide authentication commands
    prices = StreamingForexPrices(
        settings.STREAM_DOMAIN, settings.ACCESS_TOKEN, 
        settings.ACCOUNT_ID, pairs, events
    )

    # Create the strategy/signal generator, passing the 
    # instrument and the events queue
    strategy = TestStrategy(pairs, events)

    # Create the portfolio object that will be used to
    # compare the OANDA positions with the local, to
    # ensure backtesting integrity.
    portfolio = Portfolio(
        prices, events, equity=equity, backtest=False
    )

    # Create the execution handler making sure to
    # provide authentication commands
    execution = OANDAExecutionHandler(
        settings.API_DOMAIN, 
        settings.ACCESS_TOKEN, 
        settings.ACCOUNT_ID
    )
    
    # Create two separate threads: One for the trading loop
    # and another for the market price streaming class
    trade_thread = threading.Thread(
        target=trade, args=(
            events, strategy, portfolio, execution, heartbeat
        )
    )
    price_thread = threading.Thread(target=prices.stream_to_queue, args=[])
    
    # Start both threads
    logger.info("Starting trading thread")
    trade_thread.start()
    logger.info("Starting price streaming thread")
    price_thread.start()
