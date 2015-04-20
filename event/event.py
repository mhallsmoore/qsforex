class Event(object):
    pass


class BacktestEndEvent(Event):
    def __init__(self):
        self.type = 'BACKTEST_ENDED'


class TickEvent(Event):
    def __init__(self, instrument, time, bid, ask):
        self.type = 'TICK'
        self.instrument = instrument
        self.time = time
        self.bid = bid
        self.ask = ask


class SignalEvent(Event):
    def __init__(self, instrument, order_type, side):
        self.type = 'SIGNAL'
        self.instrument = instrument
        self.order_type = order_type
        self.side = side

    def __str__(self):
        return 'EventType: {0} Instrument: {1} OrderType: {2} Side:{3}'\
            .format(self.type, self.instrument, self.order_type, self.side)


class OrderEvent(Event):
    def __init__(self, instrument, units, order_type, side):
        self.type = 'ORDER'
        self.instrument = instrument
        self.units = units
        self.order_type = order_type
        self.side = side

    def __str__(self):
        return 'EventType: {0} Instrument: {1} Units: {2} OrderType: {3} Side: {4}'\
            .format(self.type, self.instrument, self.units, self.order_type, self.side)