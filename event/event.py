class Event(object):
    pass


class TickEvent(Event):
    def __init__(self, instrument, time, bid, ask):
        self.type = 'TICK'
        self.instrument = instrument
        self.time = time
        self.bid = bid
        self.ask = ask


class SignalEvent(Event):
    def __init__(self, instrument, order_type, side, time):
        self.type = 'SIGNAL'
        self.instrument = instrument
        self.order_type = order_type
        self.side = side        
        self.time = time  # Time of the last tick that generated the signal


class OrderEvent(Event):
    def __init__(self, instrument, units, order_type, side):
        self.type = 'ORDER'
        self.instrument = instrument
        self.units = units
        self.order_type = order_type
        self.side = side        
