from decimal import Decimal, getcontext, ROUND_HALF_DOWN
import unittest

from qsforex.portfolio.portfolio import Portfolio
from qsforex.portfolio.position_test import TickerMock
from qsforex.portfolio.position import Position


class TestPortfolio(unittest.TestCase):

    def setUp(self):
        home_currency = "GBP"
        leverage = 20
        equity = Decimal("100000.00")
        risk_per_trade = Decimal("0.02")
        ticker = TickerMock()
        events = {}
        self.port = Portfolio(
            ticker, events, home_currency=home_currency,
            leverage=leverage, equity=equity,
            risk_per_trade=risk_per_trade
        )

    def test_add_position_long(self):
        position_type = "long"
        currency_pair = "GBPUSD"
        units = Decimal("2000")
        ticker = TickerMock()
        self.port.add_new_position(
            position_type,
            currency_pair,
            units, ticker
        )
        ps = self.port.positions[currency_pair]

        self.assertEquals(ps.position_type, position_type)
        self.assertEquals(ps.currency_pair, currency_pair)
        self.assertEquals(ps.units, units)
        self.assertEquals(ps.avg_price, ticker.prices[currency_pair]["ask"])
        self.assertEquals(ps.cur_price, ticker.prices[currency_pair]["bid"])

    def test_add_position_short(self):
        position_type = "short"
        currency_pair = "GBPUSD"
        units = Decimal("2000")
        ticker = TickerMock()
        self.port.add_new_position(
            position_type,
            currency_pair,
            units, ticker
        )
        ps = self.port.positions[currency_pair]

        self.assertEquals(ps.position_type, position_type)
        self.assertEquals(ps.currency_pair, currency_pair)
        self.assertEquals(ps.units, units)
        self.assertEquals(ps.avg_price, ticker.prices[currency_pair]["bid"])
        self.assertEquals(ps.cur_price, ticker.prices[currency_pair]["ask"])

    def test_add_position_units_long(self):
        position_type = "long"
        currency_pair = "GBPUSD"
        units = Decimal("2000")
        ticker = TickerMock()

        # Test for no position
        alt_currency_pair = "USDCAD"
        apu = self.port.add_position_units(
            alt_currency_pair, units
        )
        self.assertFalse(apu)

        # Add a position and test for real position
        self.port.add_new_position(
            position_type,
            currency_pair,
            units, ticker
        )
        ps = self.port.positions[currency_pair]

        # Test for addition of units
        ticker.prices["GBPUSD"]["bid"] = Decimal("1.51878")
        ticker.prices["GBPUSD"]["ask"] = Decimal("1.51928")
        ticker.prices["USDGBP"]["bid"] = Decimal("0.65842")
        ticker.prices["USDGBP"]["ask"] = Decimal("0.65821")
        apu = self.port.add_position_units(
            currency_pair, units
        )
        self.assertTrue(apu)
        self.assertEqual(ps.avg_price, Decimal("1.511385"))

    def test_add_position_units_short(self):
        position_type = "short"
        currency_pair = "GBPUSD"
        units = Decimal("2000")
        ticker = TickerMock()

        # Test for no position
        alt_currency_pair = "USDCAD"
        apu = self.port.add_position_units(
            alt_currency_pair, units
        )
        self.assertFalse(apu)

        # Add a position and test for real position
        self.port.add_new_position(
            position_type,
            currency_pair,
            units, ticker
        )
        ps = self.port.positions[currency_pair]

        # Test for addition of units
        ticker.prices["GBPUSD"]["bid"] = Decimal("1.51878")
        ticker.prices["GBPUSD"]["ask"] = Decimal("1.51928")
        ticker.prices["USDGBP"]["bid"] = Decimal("0.65842")
        ticker.prices["USDGBP"]["ask"] = Decimal("0.65821")
        apu = self.port.add_position_units(
            currency_pair, units
        )
        self.assertTrue(apu)
        self.assertEqual(ps.avg_price, Decimal("1.51103"))

    def test_remove_position_units_long(self):
        position_type = "long"
        currency_pair = "GBPUSD"
        units = Decimal("2000")
        ticker = TickerMock()

        # Test for no position
        alt_currency_pair = "USDCAD"
        apu = self.port.remove_position_units(
            alt_currency_pair, units
        )
        self.assertFalse(apu)

        # Add a position and then add units to it
        self.port.add_new_position(
            position_type,
            currency_pair,
            units, ticker
        )
        ps = self.port.positions[currency_pair]
        # Test for addition of units
        ticker.prices["GBPUSD"]["bid"] = Decimal("1.51878")
        ticker.prices["GBPUSD"]["ask"] = Decimal("1.51928")
        ticker.prices["USDGBP"]["bid"] = Decimal("0.65842")
        ticker.prices["USDGBP"]["ask"] = Decimal("0.65821")

        add_units = Decimal("8000")
        apu = self.port.add_position_units(
            currency_pair, add_units
        )
        self.assertEqual(ps.units, 10000)
        self.assertEqual(ps.avg_price, Decimal("1.516122"))

        # Test removal of (some) of the units
        ticker.prices["GBPUSD"]["bid"] = Decimal("1.52017")
        ticker.prices["GBPUSD"]["ask"] = Decimal("1.52134")
        ticker.prices["USDGBP"]["bid"] = Decimal("0.65782")
        ticker.prices["USDGBP"]["ask"] = Decimal("0.65732")

        remove_units = Decimal("3000")
        rpu = self.port.remove_position_units(
            currency_pair, remove_units
        )
        self.assertTrue(rpu)
        self.assertEqual(ps.units, Decimal("7000"))
        self.assertEqual(self.port.balance, Decimal("100007.99"))

    def test_remove_position_units_short(self):
        position_type = "short"
        currency_pair = "GBPUSD"
        units = Decimal("2000")
        ticker = TickerMock()

        # Test for no position
        alt_currency_pair = "USDCAD"
        apu = self.port.remove_position_units(
            alt_currency_pair, units
        )
        self.assertFalse(apu)

        # Add a position and then add units to it
        self.port.add_new_position(
            position_type,
            currency_pair,
            units, ticker
        )
        ps = self.port.positions[currency_pair]
        # Test for addition of units
        ticker.prices["GBPUSD"]["bid"] = Decimal("1.51878")
        ticker.prices["GBPUSD"]["ask"] = Decimal("1.51928")
        ticker.prices["USDGBP"]["bid"] = Decimal("0.65842")
        ticker.prices["USDGBP"]["ask"] = Decimal("0.65821")

        add_units = Decimal("8000")
        apu = self.port.add_position_units(
            currency_pair, add_units
        )
        self.assertEqual(ps.units, 10000)
        self.assertEqual(ps.avg_price, Decimal("1.51568"))

        # Test removal of (some) of the units
        ticker.prices["GBPUSD"]["bid"] = Decimal("1.52017")
        ticker.prices["GBPUSD"]["ask"] = Decimal("1.52134")
        ticker.prices["USDGBP"]["bid"] = Decimal("0.65782")
        ticker.prices["USDGBP"]["ask"] = Decimal("0.65732")

        remove_units = Decimal("3000")
        rpu = self.port.remove_position_units(
            currency_pair, remove_units
        )
        self.assertTrue(rpu)
        self.assertEqual(ps.units, Decimal("7000"))
        self.assertEqual(self.port.balance, Decimal("99988.83"))

    def test_close_position_long(self):
        position_type = "long"
        currency_pair = "GBPUSD"
        units = Decimal("2000")
        ticker = TickerMock()

        # Test for no position
        alt_currency_pair = "USDCAD"
        apu = self.port.remove_position_units(
            alt_currency_pair, units
        )
        self.assertFalse(apu)

        # Add a position and then add units to it
        self.port.add_new_position(
            position_type,
            currency_pair,
            units, ticker
        )
        ps = self.port.positions[currency_pair]
        # Test for addition of units
        ticker.prices["GBPUSD"]["bid"] = Decimal("1.51878")
        ticker.prices["GBPUSD"]["ask"] = Decimal("1.51928")
        ticker.prices["USDGBP"]["bid"] = Decimal("0.65842")
        ticker.prices["USDGBP"]["ask"] = Decimal("0.65821")

        add_units = Decimal("8000")
        apu = self.port.add_position_units(
            currency_pair, add_units
        )
        self.assertEqual(ps.units, 10000)
        self.assertEqual(ps.avg_price, Decimal("1.516122"))

        # Test removal of (some) of the units
        ticker.prices["GBPUSD"]["bid"] = Decimal("1.52017")
        ticker.prices["GBPUSD"]["ask"] = Decimal("1.52134")
        ticker.prices["USDGBP"]["bid"] = Decimal("0.65782")
        ticker.prices["USDGBP"]["ask"] = Decimal("0.65732")

        remove_units = Decimal("3000")
        rpu = self.port.remove_position_units(
            currency_pair, remove_units
        )
        self.assertTrue(rpu)
        self.assertEqual(ps.units, Decimal("7000"))
        self.assertEqual(self.port.balance, Decimal("100007.99"))

        # Close the position
        cp = self.port.close_position(currency_pair)
        self.assertTrue(cp)
        self.assertRaises(ps)  # Key doesn't exist
        self.assertEqual(self.port.balance, Decimal("100026.63"))

    def test_close_position_short(self):
        position_type = "short"
        currency_pair = "GBPUSD"
        units = Decimal("2000")
        ticker = TickerMock()

        # Test for no position
        alt_currency_pair = "USDCAD"
        apu = self.port.remove_position_units(
            alt_currency_pair, units
        )
        self.assertFalse(apu)

        # Add a position and then add units to it
        self.port.add_new_position(
            position_type,
            currency_pair,
            units, ticker
        )
        ps = self.port.positions[currency_pair]
        # Test for addition of units
        ticker.prices["GBPUSD"]["bid"] = Decimal("1.51878")
        ticker.prices["GBPUSD"]["ask"] = Decimal("1.51928")
        ticker.prices["USDGBP"]["bid"] = Decimal("0.65842")
        ticker.prices["USDGBP"]["ask"] = Decimal("0.65821")

        add_units = Decimal("8000")
        apu = self.port.add_position_units(
            currency_pair, add_units
        )
        self.assertEqual(ps.units, 10000)
        self.assertEqual(ps.avg_price, Decimal("1.51568"))

        # Test removal of (some) of the units
        ticker.prices["GBPUSD"]["bid"] = Decimal("1.52017")
        ticker.prices["GBPUSD"]["ask"] = Decimal("1.52134")
        ticker.prices["USDGBP"]["bid"] = Decimal("0.65782")
        ticker.prices["USDGBP"]["ask"] = Decimal("0.65732")

        remove_units = Decimal("3000")
        rpu = self.port.remove_position_units(
            currency_pair, remove_units
        )
        self.assertTrue(rpu)
        self.assertEqual(ps.units, Decimal("7000"))
        self.assertEqual(self.port.balance, Decimal("99988.83"))

        # Close the position
        cp = self.port.close_position(currency_pair)
        self.assertTrue(cp)
        self.assertRaises(ps)  # Key doesn't exist
        self.assertEqual(self.port.balance, Decimal("99962.77"))


if __name__ == "__main__":
    unittest.main()
