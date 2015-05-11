from __future__ import print_function

from copy import deepcopy
from decimal import Decimal, getcontext, ROUND_HALF_DOWN
import os

import pandas as pd

from qsforex.event.event import OrderEvent
from qsforex.portfolio.position import Position
from qsforex.settings import OUTPUT_RESULTS_DIR


class Portfolio(object):
    def __init__(
        self, ticker, events, home_currency="GBP", leverage=20, 
        equity=Decimal("100000.00"), risk_per_trade=Decimal("0.02")
    ):
        self.ticker = ticker
        self.events = events
        self.home_currency = home_currency
        self.leverage = leverage
        self.equity = equity
        self.balance = deepcopy(self.equity)
        self.risk_per_trade = risk_per_trade
        self.trade_units = self.calc_risk_position_size()
        self.positions = {}
        self.equity = []

    def calc_risk_position_size(self):
        return self.equity * self.risk_per_trade

    def add_new_position(
        self, position_type, currency_pair, units, ticker
    ):
        ps = Position(
            self.home_currency, position_type, 
            currency_pair, units, ticker
        )
        self.positions[currency_pair] = ps

    def add_position_units(self, currency_pair, units):
        if currency_pair not in self.positions:
            return False
        else:
            ps = self.positions[currency_pair]
            ps.add_units(units)
            return True

    def remove_position_units(self, currency_pair, units):
        if currency_pair not in self.positions:
            return False
        else:
            ps = self.positions[currency_pair]
            pnl = ps.remove_units(units)
            self.balance += pnl
            return True

    def close_position(self, currency_pair):
        if currency_pair not in self.positions:
            return False
        else:
            ps = self.positions[currency_pair]
            pnl = ps.close_position()
            self.balance += pnl
            del[self.positions[currency_pair]]
            return True

    def append_equity_row(self, time, balance):
        d = {"time": time, "balance": balance}
        self.equity.append(d)

    def output_results(self):
        filename = "equity.csv"
        out_file = os.path.join(OUTPUT_RESULTS_DIR, filename)
        df_equity = pd.DataFrame.from_records(self.equity, index='time')
        df_equity.to_csv(out_file)
        print("Simulation complete and results exported to %s" % filename)

    def execute_signal(self, signal_event):       
        side = signal_event.side
        currency_pair = signal_event.instrument
        units = int(self.trade_units)
        time = signal_event.time
        
        # If there is no position, create one
        if currency_pair not in self.positions:
            if side == "buy":
                position_type = "long"
            else:
                position_type = "short"
            self.add_new_position(
                position_type, currency_pair, 
                units, self.ticker
            )

        # If a position exists add or remove units
        else:
            ps = self.positions[currency_pair]

            if side == "buy" and ps.position_type == "long":
                add_position_units(currency_pair, units)

            elif side == "sell" and ps.position_type == "long":
                if units == ps.units:
                    self.close_position(currency_pair)
                # TODO: Allow units to be added/removed
                elif units < ps.units:
                    return
                elif units > ps.units:
                    return

            elif side == "buy" and ps.position_type == "short":
                if units == ps.units:
                    self.close_position(currency_pair)
                # TODO: Allow units to be added/removed
                elif units < ps.units:
                    return
                elif units > ps.units:
                    return
                    
            elif side == "sell" and ps.position_type == "short":
                add_position_units(currency_pair, units)

        order = OrderEvent(currency_pair, units, "market", side)
        self.events.put(order)

        print("Balance: %0.2f" % self.balance)
        self.append_equity_row(time, self.balance)
        