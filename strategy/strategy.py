from qsforex.event.event import SignalEvent


class TestRandomStrategy(object):
    def __init__(self, instrument, events):
        self.instrument = instrument
        self.events = events
        self.ticks = 0

    def calculate_signals(self, event):
        if event.type == 'TICK':
            self.ticks += 1
            if self.ticks == 2:
                signal = SignalEvent(self.instrument, "market", "buy")
                self.events.put(signal)
            if self.ticks == 10:
                signal = SignalEvent(self.instrument, "market", "sell")
                self.events.put(signal)
