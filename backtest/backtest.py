from __future__ import print_function

try:
    import Queue as queue
except ImportError:
    import queue
import time

from qsforex import settings


class Backtest(object):
    """
    Enscapsulates the settings and components for carrying out
    an event-driven backtest on the foreign exchange markets.
    """
    def __init__(
        self, pairs, data_handler, strategy, 
        strategy_params, portfolio, execution, 
        equity=100000.0, heartbeat=0.0, 
        max_iters=10000000000
    ):
        """
        Initialises the backtest.
        """
        import ipdb; ipdb.set_trace()
        self.pairs = pairs
        self.events = queue.PriorityQueue()
        self.csv_dir = settings.CSV_DATA_DIR
        self.ticker = data_handler(self.pairs, self.events, self.csv_dir)
        self.strategy_params = strategy_params
        self.strategy = strategy(
            self.pairs, self.events, **self.strategy_params
        )
        self.equity = equity
        self.heartbeat = heartbeat
        self.max_iters = max_iters
        self.portfolio = portfolio(
            self.ticker, self.events, equity=self.equity, backtest=True
        )
        self.execution = execution()

    def _run_backtest(self):
        """
        Carries out an infinite while loop that polls the 
        events queue and directs each event to either the
        strategy component of the execution handler. The
        loop will then pause for "heartbeat" seconds and
        continue unti the maximum number of iterations is
        exceeded.
        """
        print("Running Backtest...")
        iters = 0
        while iters < self.max_iters and self.ticker.continue_backtest:
            try:
                event = self.events.get(False)
            except queue.Empty:
                self.ticker.stream_next_tick()
            else:
                if event is not None:
                    if event[1].type == 'TICK':
                        self.strategy.calculate_signals(event[1])
                        self.portfolio.update_portfolio(event[1])
                    elif event[1].type == 'SIGNAL':
                        self.portfolio.execute_signal(event[1])
                    elif event[1].type == 'ORDER':
                        self.execution.execute_order(event[1])
            time.sleep(self.heartbeat)
            iters += 1

    def _output_performance(self):
        """
        Outputs the strategy performance from the backtest.
        """
        print("Calculating Performance Metrics...")
        self.portfolio.output_results()

    def simulate_trading(self):
        """
        Simulates the backtest and outputs portfolio performance.
        """
        self._run_backtest()
        self._output_performance()
        print("Backtest complete.")
