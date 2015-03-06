from qsforex.event.event import SignalEvent


class TestStrategy(object):
    def __init__(self, instrument, events):
        self.instrument = instrument
        self.events = events
        self.ticks = 0
        self.invested = False

    def calculate_signals(self, event):
        if event.type == 'TICK':
            self.ticks += 1
            if self.ticks % 5 == 0:
                if self.invested == False:
                    signal = SignalEvent(self.instrument, "market", "buy")
                    self.events.put(signal)
                    self.invested = True
                else:
                    signal = SignalEvent(self.instrument, "market", "sell")
                    self.events.put(signal)
                    self.invested = False
                    