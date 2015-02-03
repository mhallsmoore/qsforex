from copy import deepcopy

from qsforex.event.event import OrderEvent
from qsforex.portfolio.position import Position


class Portfolio(object):
    def __init__(
        self, ticker, events, base="GBP", leverage=20, 
        equity=100000.0, risk_per_trade=0.02
    ):
        self.ticker = ticker
        self.events = events
        self.base = base
        self.leverage = leverage
        self.equity = equity
        self.balance = deepcopy(self.equity)
        self.risk_per_trade = risk_per_trade
        self.trade_units = 100000#self.calc_risk_position_size()
        self.positions = {}

    def calc_risk_position_size(self):
        return self.equity * self.risk_per_trade

    def add_new_position(
        self, side, market, units, exposure,
        add_price, remove_price
    ):
        ps = Position(
            side, market, units, exposure,
            add_price, remove_price
        )
        self.positions[market] = ps

    def add_position_units(
        self, market, units, exposure, 
        add_price, remove_price
    ):
        if market not in self.positions:
            return False
        else:
            ps = self.positions[market]
            new_total_units = ps.units + units
            new_total_cost = ps.avg_price*ps.units + add_price*units
            ps.exposure += exposure
            ps.avg_price = new_total_cost/new_total_units
            ps.units = new_total_units
            ps.update_position_price(remove_price)
            return True

    def remove_position_units(
        self, market, units, remove_price
    ):
        if market not in self.positions:
            return False
        else:
            ps = self.positions[market]
            ps.units -= units
            exposure = float(units)
            ps.exposure -= exposure
            ps.update_position_price(remove_price)
            pnl = ps.calculate_pips() * exposure / remove_price 
            self.balance += pnl
            return True

    def close_position(
        self, market, remove_price
    ):
        if market not in self.positions:
            return False
        else:
            ps = self.positions[market]
            ps.update_position_price(remove_price)
            pnl = ps.calculate_pips() * ps.exposure / remove_price 
            self.balance += pnl
            del[self.positions[market]]
            return True

    def execute_signal(self, signal_event):
        side = signal_event.side
        market = signal_event.instrument
        units = int(self.trade_units)

        # Check side for correct bid/ask prices
        #if side == "buy":
        add_price = self.ticker.cur_ask
        remove_price = self.ticker.cur_bid
        #else:
            #add_price = self.ticker.cur_bid
            #remove_price = self.ticker.cur_ask
        exposure = float(units)

        # If there is no position, create one
        if market not in self.positions:
            self.add_new_position(
                side, market, units, exposure,
                add_price, remove_price
            )
            order = OrderEvent(market, units, "market", "buy")
            self.events.put(order)
        # If a position exists add or remove units
        else:
            ps = self.positions[market]
            # Check if the sides equal
            if side == ps.side:
                # Add to the position
                add_position_units(
                    market, units, exposure,
                    add_price, remove_price
                )
            else:
                # Check if the units close out the position
                if units == ps.units:
                    # Close the position
                    self.close_position(market, remove_price)
                    order = OrderEvent(market, units, "market", "sell")
                    self.events.put(order)
                elif units < ps.units:
                    # Remove from the position
                    self.remove_position_units(
                        market, units, remove_price
                    )
                else: # units > ps.units
                    # Close the position and add a new one with
                    # additional units of opposite side
                    new_units = units - ps.units
                    self.close_position(market, remove_price)
                    
                    if side == "buy":
                        new_side = "sell"
                    else:
                        new_side = "sell"
                    new_exposure = float(units)
                    self.add_new_position(
                        new_side, market, new_units, 
                        new_exposure, add_price, remove_price
                    )
        print "Balance: %0.2f" % self.balance