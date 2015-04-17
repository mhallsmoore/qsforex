from copy import deepcopy
from decimal import Decimal, getcontext, ROUND_HALF_DOWN

from qsforex.event.event import OrderEvent
from qsforex.portfolio.position import Position


class Portfolio(object):
    def __init__(
        self, ticker, events, base="GBP", leverage=20, 
        equity=Decimal("100000.00"), risk_per_trade=Decimal("0.02")
    ):
        self.ticker = ticker
        self.events = events
        self.base = base
        self.leverage = leverage
        self.equity = equity
        self.balance = deepcopy(self.equity)
        self.risk_per_trade = risk_per_trade
        self.trade_units = self.calc_risk_position_size()
        self.positions = {}

    def calc_risk_position_size(self):
        return self.equity * self.risk_per_trade

    def add_new_position(
        self, position_type, market, units, 
        exposure, bid, ask
    ):
        ps = Position(
            position_type, market, units, 
            exposure, bid, ask
        )
        self.positions[market] = ps

    def add_position_units(
        self, market, units, 
        exposure, bid, ask
    ):
        if market not in self.positions:
            return False
        else:
            ps = self.positions[market]
            if ps.position_type == "long":
                add_price = ask
            else:
                add_price = bid
            new_total_units = ps.units + units
            new_total_cost = ps.avg_price*ps.units + add_price*units
            ps.exposure += exposure
            ps.avg_price = new_total_cost/new_total_units
            ps.units = new_total_units
            ps.update_position_price(bid, ask, exposure)
            return True

    def remove_position_units(
        self, market, units, bid, ask
    ):
        if market not in self.positions:
            return False
        else:
            ps = self.positions[market]
            if ps.position_type == "long":
                remove_price = bid
            else:
                remove_price = ask
            ps.units -= units
            exposure = Decimal(str(units))
            ps.exposure -= exposure
            ps.update_position_price(bid, ask, exposure)
            pnl = ps.calculate_pips() * exposure / remove_price 
            self.balance += pnl.quantize(Decimal("0.01", ROUND_HALF_DOWN))
            return True

    def close_position(
        self, market, bid, ask
    ):
        if market not in self.positions:
            return False
        else:
            ps = self.positions[market]
            ps.update_position_price(bid, ask, ps.exposure)
            if ps.position_type == "long":
                remove_price = bid
            else:
                remove_price = ask
            pnl = ps.calculate_pips() * ps.exposure / remove_price 
            self.balance += pnl.quantize(Decimal("0.01", ROUND_HALF_DOWN))
            del[self.positions[market]]
            return True

    def execute_signal(self, signal_event):       
        side = signal_event.side
        market = signal_event.instrument
        units = int(self.trade_units)
        exposure = Decimal(str(units))
        bid = Decimal(str(self.ticker.cur_bid))
        ask = Decimal(str(self.ticker.cur_ask))

        # If there is no position, create one
        if market not in self.positions:
            if side == "buy":
                position_type = "long"
            else:
                position_type = "short"
            self.add_new_position(
                position_type, market, units, 
                exposure, bid, ask
            )

        # If a position exists add or remove units
        else:
            ps = self.positions[market]

            if side == "buy" and ps.position_type == "long":
                add_position_units(market, units, exposure, bid, ask)

            elif side == "sell" and ps.position_type == "long":
                if units == ps.units:
                    self.close_position(market, bid, ask)
                # TODO: Allow units to be added/removed
                elif units < ps.units:
                    return
                elif units > ps.units:
                    return

            elif side == "buy" and ps.position_type == "short":
                if units == ps.units:
                    self.close_position(market, bid, ask)
                # TODO: Allow units to be added/removed
                elif units < ps.units:
                    return
                elif units > ps.units:
                    return
                    
            elif side == "sell" and ps.position_type == "short":
                add_position_units(market, units, exposure, bid, ask)

        order = OrderEvent(market, units, "market", side)
        self.events.put(order)

        print "Balance: %0.2f" % self.balance