import copy
import Queue
import threading
import time
from decimal import Decimal, getcontext

from qsforex.execution.execution import Execution
from qsforex.portfolio.portfolio import Portfolio
from qsforex.settings import STREAM_DOMAIN, API_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID
from qsforex.strategy.strategy import TestStrategy
from qsforex.streaming.streaming import StreamingForexPrices


def trade(events, strategy, portfolio, execution):
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
                elif event.type == 'ORDER':
                    execution.execute_order(event)
        time.sleep(heartbeat)


if __name__ == "__main__":
    # Set the number of decimal places to 2
    getcontext().prec = 2

    heartbeat = 0.5  # Half a second between polling
    events = Queue.Queue()
    equity = Decimal("99949.82")

    # Trade "Cable"
    instrument = "GBP_USD"

    # Create the OANDA market price streaming class
    # making sure to provide authentication commands
    prices = StreamingForexPrices(
        STREAM_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID,
        instrument, events
    )

    # Create the strategy/signal generator, passing the 
    # instrument and the events queue
    strategy = TestStrategy(instrument, events)

    # Create the portfolio object that will be used to
    # compare the OANDA positions with the local, to
    # ensure backtesting integrity.
    portfolio = Portfolio(prices, events, equity=equity)

    # Create the execution handler making sure to
    # provide authentication commands
    execution = Execution(API_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID)
    
    # Create two separate threads: One for the trading loop
    # and another for the market price streaming class
    trade_thread = threading.Thread(
        target=trade, args=(
            events, strategy, portfolio, execution
        )
    )
    price_thread = threading.Thread(target=prices.stream_to_queue, args=[])
    
    # Start both threads
    trade_thread.start()
    price_thread.start()