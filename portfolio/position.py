from decimal import Decimal, getcontext, ROUND_HALF_DOWN


class Position(object):
    def __init__(
        self, position_type, market, 
        units, exposure, bid, ask
    ):
        self.position_type = position_type  # Long or short
        self.market = market
        self.units = units
        self.exposure = Decimal(str(exposure))

        # Long or short
        if self.position_type == "long":
            self.avg_price = Decimal(str(ask))
            self.cur_price = Decimal(str(bid))
        else:
            self.avg_price = Decimal(str(bid))
            self.cur_price = Decimal(str(ask))

        self.profit_base = self.calculate_profit_base(self.exposure)
        self.profit_perc = self.calculate_profit_perc(self.exposure)

    def calculate_pips(self):
        getcontext.prec = 6
        mult = Decimal("1")
        if self.position_type == "long":
            mult = Decimal("1")
        elif self.position_type == "short":
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

    def update_position_price(self, bid, ask, exposure):
        if self.position_type == "long":
            self.cur_price = Decimal(str(bid))
        else:
            self.cur_price = Decimal(str(ask))
        self.profit_base = self.calculate_profit_base(exposure)
        self.profit_perc = self.calculate_profit_perc(exposure)
