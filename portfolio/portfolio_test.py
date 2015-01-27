import unittest

#from position import Position
from portfolio import Portfolio


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        base = "GBP"
        leverage = 20
        equity = 100000.0
        risk_per_trade = 0.02
        ticker = {}
        self.port = Portfolio(
            ticker, base=base, leverage=leverage, 
            equity=equity, risk_per_trade=risk_per_trade
        )

    def test_add_position(self):
        side = "LONG"
        market = "GBP/USD"
        units = 2000
        exposure = float(units)
        add_price = 1.51819
        remove_price = 1.51770

        self.port.add_new_position(
            side, market, units, exposure,
            add_price, remove_price
        )
        ps = self.port.positions[market]

        self.assertEquals(ps.side, side)
        self.assertEquals(ps.market, market)
        self.assertEquals(ps.units, units)
        self.assertEquals(ps.exposure, exposure)
        self.assertEquals(ps.avg_price, add_price)
        self.assertEquals(ps.cur_price, remove_price)

    def test_add_position_units(self):
        side = "LONG"
        units = 2000
        exposure = float(units)
        add_price = 1.51928
        remove_price = 1.51878

        # Test for no position
        market = "EUR/USD"
        apu = self.port.add_position_units(
            market, units, exposure,
            add_price, remove_price
        )
        self.assertFalse(apu)

        # Test for real position
        market = "GBP/USD"
        apu = self.port.add_position_units(
            market, units, exposure,
            add_price, remove_price
        )
        self.assertTrue(apu)
        ps = self.port.positions[market]

        self.assertAlmostEqual(ps.avg_price, 1.518735)


if __name__ == "__main__":
    unittest.main()