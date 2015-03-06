from decimal import Decimal, getcontext
import unittest

from position import Position


class TestLongGBPUSDPosition(unittest.TestCase):
    def setUp(self):
        getcontext.prec = 2
        side = "LONG"
        market = "GBP/USD"
        units = 2000
        exposure = Decimal("2000.00")
        avg_price = Decimal("1.51819")
        cur_price = Decimal("1.51770")
        self.position = Position(
            side, market, units, exposure,
            avg_price, cur_price
        )

    def test_calculate_pips(self):
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("-0.00049"))

    def test_calculate_profit_base(self):
        profit_base = self.position.calculate_profit_base()
        #self.assertEqual(profit_base, Decimal("-0.6457139"))
        self.assertEqual(profit_base, Decimal("-0.64571"))

    def test_calculate_profit_perc(self):
        profit_perc = self.position.calculate_profit_perc()
        #self.assertEqual(profit_perc, Decimal("-0.032285695"))
        self.assertEqual(profit_perc, Decimal("-0.03229"))


class TestShortGBPUSDPosition(unittest.TestCase):
    def setUp(self):
        getcontext.prec = 2
        side = "SHORT"
        market = "GBP/USD"
        units = 2000
        exposure = Decimal("2000.00")
        avg_price = Decimal("1.51819")
        cur_price = Decimal("1.51770")
        self.position = Position(
            side, market, units, exposure,
            avg_price, cur_price
        )

    def test_calculate_pips(self):
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("0.00049"))

    def test_calculate_profit_base(self):
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("0.64571"))

    def test_calculate_profit_perc(self):
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("0.03229"))


if __name__ == "__main__":
    unittest.main()