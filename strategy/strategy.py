import copy

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
        if event.type == 'TICK' and event.instrument == self.pairs[0]:
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
        self.pairs_dict = self.create_pairs_dict()
        self.events = events      
        self.short_window = short_window
        self.long_window = long_window

    def create_pairs_dict(self):
        attr_dict = {
            "ticks": 0,
            "invested": False,
            "short_sma": None,
            "long_sma": None
        }
        pairs_dict = {}
        for p in self.pairs:
            pairs_dict[p] = copy.deepcopy(attr_dict)
        return pairs_dict

    def calc_rolling_sma(self, sma_m_1, window, price):
        return ((sma_m_1 * (window - 1)) + price) / window

    def calculate_signals(self, event):
        if event.type == 'TICK':
            pair = event.instrument
            price = event.bid
            pd = self.pairs_dict[pair]
            if pd["ticks"] == 0:
                pd["short_sma"] = price
                pd["long_sma"] = price
            else:
                pd["short_sma"] = self.calc_rolling_sma(
                    pd["short_sma"], self.short_window, price
                )
                pd["long_sma"] = self.calc_rolling_sma(
                    pd["long_sma"], self.long_window, price
                )
            # Only start the strategy when we have created an accurate short window
            if pd["ticks"] > self.short_window:
                if pd["short_sma"] > pd["long_sma"] and not pd["invested"]:
                    signal = SignalEvent(pair, "market", "buy", event.time)
                    self.events.put(signal)
                    pd["invested"] = True
                if pd["short_sma"] < pd["long_sma"] and pd["invested"]:
                    signal = SignalEvent(pair, "market", "sell", event.time)
                    self.events.put(signal)
                    pd["invested"] = False
            pd["ticks"] += 1