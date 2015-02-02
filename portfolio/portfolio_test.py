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
        market = "GBP/USD"
        units = 2000
        exposure = float(units)
        add_price = 1.51819
        remove_price = 1.51770

        # Test for no position
        market = "EUR/USD"
        apu = self.port.add_position_units(
            market, units, exposure,
            add_price, remove_price
        )
        self.assertFalse(apu)

        # Add a position and test for real position
        market = "GBP/USD"        
        self.port.add_new_position(
            side, market, units, exposure,
            add_price, remove_price
        )
        ps = self.port.positions[market]

        # Test for addition of units
        add_price = 1.51928
        remove_price = 1.51878
        apu = self.port.add_position_units(
            market, units, exposure,
            add_price, remove_price
        )
        self.assertTrue(apu)
        self.assertAlmostEqual(ps.avg_price, 1.518735)

    def test_remove_position_units(self):
        side = "LONG"
        units = 2000
        exposure = float(units)
        add_price = 1.51819
        remove_price = 1.51770

        # Test for no position
        market = "EUR/USD"
        apu = self.port.remove_position_units(
            market, units, remove_price
        )
        self.assertFalse(apu)

        # Add a position and then add units to it
        market = "GBP/USD"        
        self.port.add_new_position(
            side, market, units, exposure,
            add_price, remove_price
        )
        ps = self.port.positions[market]
        add_price = 1.51928
        remove_price = 1.51878
        add_units = 8000
        add_exposure = float(add_units)
        apu = self.port.add_position_units(
            market, add_units, add_exposure,
            add_price, remove_price
        )
        self.assertEqual(ps.units, 10000)
        self.assertEqual(ps.exposure, 10000.0)
        self.assertAlmostEqual(ps.avg_price, 1.519062)

        # Test removal of (some) of the units
        add_price = 1.52134
        remove_price = 1.52017
        remove_units = 3000
        rpu = self.port.remove_position_units(
            market, remove_units, remove_price
        )
        self.assertTrue(rpu)
        self.assertEqual(ps.units, 7000)
        self.assertEqual(ps.exposure, 7000.0)
        self.assertAlmostEqual(ps.profit_base, 5.102060953709626)
        self.assertAlmostEqual(self.port.balance, 100002.18659755158)

    def test_close_position(self):
        side = "LONG"
        units = 2000
        exposure = float(units)
        add_price = 1.51819
        remove_price = 1.51770

        # Test for no position
        market = "EUR/USD"
        cp = self.port.close_position(
            market, remove_price
        )
        self.assertFalse(cp)

        # Add a position and then close it
        # Will lose money on the spread
        market = "GBP/USD" 
        self.port.add_new_position(
            side, market, units, exposure,
            add_price, remove_price
        )
        ps = self.port.positions[market]
        cp = self.port.close_position(
            market, remove_price
        )
        self.assertTrue(cp)
        self.assertRaises(ps)  # Key doesn't exist
        self.assertAlmostEqual(self.port.balance, 99999.35428609079)

        # Add 2000, add another 8000, remove 3000 and then 
        # close the position. Balance should be as expected 
        # for a multi-leg transaction.
        self.port.add_new_position(
            side, market, units, exposure,
            add_price, remove_price
        )
        ps = self.port.positions[market]
        add_price = 1.51928
        remove_price = 1.51878
        add_units = 8000
        add_exposure = float(add_units)
        apu = self.port.add_position_units(
            market, add_units, add_exposure,
            add_price, remove_price
        )
        self.assertEqual(ps.units, 10000)
        self.assertEqual(ps.exposure, 10000.0)
        self.assertAlmostEqual(ps.avg_price, 1.519062)
        add_price = 1.52134
        remove_price = 1.52017
        remove_units = 3000
        rpu = self.port.remove_position_units(
            market, remove_units, remove_price
        )
        self.assertEqual(ps.units, 7000)
        self.assertEqual(ps.exposure, 7000.0)
        self.assertAlmostEqual(ps.profit_base, 5.102060953709626)
        self.assertAlmostEqual(self.port.balance, 100001.54088364237)
        cp = self.port.close_position(
            market, remove_price
        )
        self.assertTrue(cp)
        self.assertRaises(ps)  # Key doesn't exist
        self.assertAlmostEqual(self.port.balance, 100006.64294459608)


if __name__ == "__main__":
    unittest.main()