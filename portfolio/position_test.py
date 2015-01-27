import unittest

from position import Position


class TestLongGBPUSDPosition(unittest.TestCase):
    def setUp(self):
        side = "LONG"
        market = "GBP/USD"
        units = 2000
        exposure = 2000.0
        avg_price = 1.51819
        cur_price = 1.51770
        self.position = Position(
            side, market, units, exposure,
            avg_price, cur_price
        )

    def test_calculate_pips(self):
        pos_pips = self.position.calculate_pips()
        self.assertAlmostEqual(pos_pips, -0.00049)

    def test_calculate_profit_base(self):
        profit_base = self.position.calculate_profit_base()
        self.assertAlmostEqual(profit_base, -0.6457139)

    def test_calculate_profit_perc(self):
        profit_perc = self.position.calculate_profit_perc()
        self.assertAlmostEqual(profit_perc, -0.032285695)


class TestShortGBPUSDPosition(unittest.TestCase):
    def setUp(self):
        side = "SHORT"
        market = "GBP/USD"
        units = 2000
        exposure = 2000.0
        avg_price = 1.51819
        cur_price = 1.51770
        self.position = Position(
            side, market, units, exposure,
            avg_price, cur_price
        )

    def test_calculate_pips(self):
        pos_pips = self.position.calculate_pips()
        self.assertAlmostEqual(pos_pips, 0.00049)

    def test_calculate_profit_base(self):
        profit_base = self.position.calculate_profit_base()
        self.assertAlmostEqual(profit_base, 0.6457139)

    def test_calculate_profit_perc(self):
        profit_perc = self.position.calculate_profit_perc()
        self.assertAlmostEqual(profit_perc, 0.032285695)


if __name__ == "__main__":
    unittest.main()