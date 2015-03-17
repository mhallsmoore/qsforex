from decimal import Decimal, getcontext, ROUND_HALF_DOWN
import unittest

from portfolio import Portfolio


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        base = "GBP"
        leverage = 20
        equity = Decimal("100000.00")
        risk_per_trade = Decimal("0.02")
        ticker = {}
        events = {}
        self.port = Portfolio(
            ticker, events, base=base, leverage=leverage,
            equity=equity, risk_per_trade=risk_per_trade
        )

    def test_add_position_long(self):
        side = "LONG"
        market = "GBP/USD"
        units = 2000
        exposure = Decimal(str(units))
        add_price = Decimal("1.51819")
        remove_price = Decimal("1.51770")

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

    def test_add_position_short(self):
        side = "SHORT"
        market = "GBP/USD"
        units = 2000
        exposure = Decimal(str(units))
        add_price = Decimal("1.51770")
        remove_price = Decimal("1.51819")

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

    def test_add_position_units_long(self):
        side = "LONG"
        market = "GBP/USD"
        units = 2000
        exposure = Decimal(str(units))
        add_price = Decimal("1.51819")
        remove_price = Decimal("1.51770")

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
        add_price = Decimal("1.51928")
        remove_price = Decimal("1.51878")
        apu = self.port.add_position_units(
            market, units, exposure,
            add_price, remove_price
        )
        self.assertTrue(apu)
        self.assertEqual(ps.avg_price, Decimal("1.518735"))

    def test_add_position_units_short(self):
        side = "SHORT"
        market = "GBP/USD"
        units = 2000
        exposure = Decimal(str(units))
        add_price = Decimal("1.51770")
        remove_price = Decimal("1.51819")

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
        add_price = Decimal("1.51878")
        remove_price = Decimal("1.51928")
        apu = self.port.add_position_units(
            market, units, exposure,
            add_price, remove_price
        )
        self.assertTrue(apu)
        self.assertEqual(ps.avg_price, Decimal("1.51824"))

    def test_remove_position_units_long(self):
        side = "LONG"
        units = 2000
        exposure = Decimal(str(units))
        add_price = Decimal("1.51819")
        remove_price = Decimal("1.51770")

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
        add_price = Decimal("1.51928")
        remove_price = Decimal("1.51878")
        add_units = 8000
        add_exposure = Decimal(str(add_units))
        apu = self.port.add_position_units(
            market, add_units, add_exposure,
            add_price, remove_price
        )
        self.assertEqual(ps.units, 10000)
        self.assertEqual(ps.exposure, Decimal("10000.00"))
        self.assertEqual(ps.avg_price, Decimal("1.519062"))

        # Test removal of (some) of the units
        add_price = Decimal("1.52134")
        remove_price = Decimal("1.52017")
        remove_units = 3000
        rpu = self.port.remove_position_units(
            market, remove_units, remove_price
        )
        self.assertTrue(rpu)
        self.assertEqual(ps.units, 7000)
        self.assertEqual(ps.exposure, Decimal("7000.00"))
        self.assertEqual(ps.profit_base, Decimal("2.19054"))
        self.assertEqual(self.port.balance, Decimal("100002.19"))

    def test_remove_position_units_short(self):
        side = "SHORT"
        units = 2000
        exposure = Decimal(str(units))
        add_price = Decimal("1.51770")
        remove_price = Decimal("1.51819")

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
        add_price = Decimal("1.51878")
        remove_price = Decimal("1.51928")
        add_units = 8000
        add_exposure = Decimal(str(add_units))
        apu = self.port.add_position_units(
            market, add_units, add_exposure,
            add_price, remove_price
        )
        self.assertEqual(ps.units, 10000)
        self.assertEqual(ps.exposure, Decimal("10000.00"))
        self.assertEqual(ps.avg_price, Decimal("1.518564"))

        # Test removal of (some) of the units
        add_price = Decimal("1.52017")
        remove_price = Decimal("1.52134")
        remove_units = 3000
        rpu = self.port.remove_position_units(
            market, remove_units, remove_price
        )
        self.assertTrue(rpu)
        self.assertEqual(ps.units, 7000)
        self.assertEqual(ps.exposure, Decimal("7000.00"))
        self.assertEqual(ps.profit_base, Decimal("-5.48201"))
        self.assertEqual(self.port.balance, Decimal("99994.52"))

    def test_close_position_long(self):
        side = "LONG"
        units = 2000
        exposure = Decimal(str(units))
        add_price = Decimal("1.51819")
        remove_price = Decimal("1.51770")

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
        self.assertEqual(self.port.balance, Decimal("99999.35"))

        # Add 2000, add another 8000, remove 3000 and then 
        # close the position. Balance should be as expected 
        # for a multi-leg transaction.
        self.port.add_new_position(
            side, market, units, exposure,
            add_price, remove_price
        )
        ps = self.port.positions[market]
        add_price = Decimal("1.51928")
        remove_price = Decimal("1.51878")
        add_units = 8000
        add_exposure = Decimal(str(add_units))
        apu = self.port.add_position_units(
            market, add_units, add_exposure,
            add_price, remove_price
        )
        self.assertEqual(ps.units, 10000)
        self.assertEqual(ps.exposure, Decimal("10000.00"))
        self.assertEqual(ps.avg_price, Decimal("1.519062"))
        add_price = Decimal("1.52134")
        remove_price = Decimal("1.52017")
        remove_units = 3000
        rpu = self.port.remove_position_units(
            market, remove_units, remove_price
        )
        self.assertEqual(ps.units, 7000)
        self.assertEqual(ps.exposure, Decimal("7000.00"))
        self.assertEqual(ps.profit_base, Decimal("2.19054"))
        self.assertEqual(self.port.balance, Decimal("100001.54"))
        cp = self.port.close_position(
            market, remove_price
        )
        self.assertTrue(cp)
        self.assertRaises(ps)  # Key doesn't exist
        self.assertEqual(self.port.balance, Decimal("100006.65"))


if __name__ == "__main__":
    unittest.main()