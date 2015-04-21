from qsforex.event.event import SignalEvent


class TestStrategy(object):
    """
    A testing strategy that alternates between buying and selling
    a currency pair on every 5th tick. This has the effect of
    continuously "crossing the spread" and so will be loss-making
    strategy. 

    It is used to test that the backtester/live trading system is
    behaving as expected.
    """
    def __init__(self, pairs, events):
        self.pairs = pairs
        self.events = events
        self.ticks = 0
        self.invested = False

    def calculate_signals(self, event):
        if event.type == 'TICK':
            if self.ticks % 5 == 0:
                if self.invested == False:
                    signal = SignalEvent(self.pairs[0], "market", "buy", event.time)
                    self.events.put(signal)
                    self.invested = True
                else:
                    signal = SignalEvent(self.pairs[0], "market", "sell", event.time)
                    self.events.put(signal)
                    self.invested = False
            self.ticks += 1


class MovingAverageCrossStrategy(object):
    """
    A basic Moving Average Crossover strategy that generates
    two simple moving averages (SMA), with default windows
    of 500 ticks for the short SMA and 2,000 ticks for the
    long SMA.

    The strategy is "long only" in the sense it will only
    open a long position once the short SMA exceeds the long
    SMA. It will close the position (by taking a corresponding
    sell order) when the long SMA recrosses the short SMA.

    The strategy uses a rolling SMA calculation in order to
    increase efficiency by eliminating the need to call two
    full moving average calculations on each tick.
    """
    def __init__(
        self, pairs, events, 
        short_window=500, long_window=2000
    ):
        self.pairs = pairs
        self.events = events
        self.ticks = 0
        self.invested = False
        
        self.short_window = short_window
        self.long_window = long_window
        self.short_sma = None
        self.long_sma = None

    def calc_rolling_sma(self, sma_m_1, window, price):
        return ((sma_m_1 * (window - 1)) + price) / window

    def calculate_signals(self, event):
        if event.type == 'TICK':
            price = event.bid
            if self.ticks == 0:
                self.short_sma = price
                self.long_sma = price
            else:
                self.short_sma = self.calc_rolling_sma(
                    self.short_sma, self.short_window, price
                )
                self.long_sma = self.calc_rolling_sma(
                    self.long_sma, self.long_window, price
                )
            # Only start the strategy when we have created an accurate short window
            if self.ticks > self.short_window:
                if self.short_sma > self.long_sma and not self.invested:
                    signal = SignalEvent(self.pairs[0], "market", "buy", event.time)
                    self.events.put(signal)
                    self.invested = True
                if self.short_sma < self.long_sma and self.invested:
                    signal = SignalEvent(self.pairs[0], "market", "sell", event.time)
                    self.events.put(signal)
                    self.invested = False
            self.ticks += 1