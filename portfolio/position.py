from decimal import Decimal, getcontext, ROUND_HALF_DOWN


class Position(object):
    def __init__(
        self, side, market, units, 
        exposure, avg_price, cur_price
    ):
        self.side = side
        self.market = market
        self.units = units
        self.exposure = Decimal(str(exposure))
        self.avg_price = Decimal(str(avg_price))
        self.cur_price = Decimal(str(cur_price))
        self.profit_base = self.calculate_profit_base(self.exposure)
        self.profit_perc = self.calculate_profit_perc(self.exposure)

    def calculate_pips(self):
        getcontext.prec = 6
        mult = Decimal("1")
        if self.side == "SHORT":
            mult = Decimal("-1")
        return (mult * (self.cur_price - self.avg_price)).quantize(
            Decimal("0.00001"), ROUND_HALF_DOWN
        )

    def calculate_profit_base(self, exposure):
        pips = self.calculate_pips()        
        return (pips * exposure / self.cur_price).quantize(
            Decimal("0.00001"), ROUND_HALF_DOWN
        )

    def calculate_profit_perc(self, exposure):
        return (self.profit_base / exposure * Decimal("100.00")).quantize(
            Decimal("0.00001"), ROUND_HALF_DOWN
        )

    def update_position_price(self, cur_price, exposure):
        self.cur_price = cur_price
        self.profit_base = self.calculate_profit_base(exposure)
        self.profit_perc = self.calculate_profit_perc(exposure)

