from decimal import Decimal, getcontext
import unittest

from position import Position


class TestLongGBPUSDPosition(unittest.TestCase):
    def setUp(self):
        getcontext.prec = 2
        position_type = "long"
        market = "GBP/USD"
        units = Decimal("2000")
        exposure = Decimal("2000.00")
        bid = Decimal("1.50328")
        ask = Decimal("1.50349")
        self.position = Position(
            position_type, market, 
            units, exposure, bid, ask
        )

    def test_calculate_init_pips(self):
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("-0.00021"))

    def test_calculate_init_profit_base(self):
        profit_base = self.position.calculate_profit_base(self.position.exposure)
        self.assertEqual(profit_base, Decimal("-0.27939"))

    def test_calculate_init_profit_perc(self):
        profit_perc = self.position.calculate_profit_perc(self.position.exposure)
        self.assertEqual(profit_perc, Decimal("-0.01397"))

    def test_calculate_updated_values(self):
        """
        Check that after the bid/ask prices move, that the updated
        pips, profit and percentage profit calculations are correct.
        """
        bid = Decimal("1.50486")
        ask = Decimal("1.50586")
        self.position.update_position_price(bid, ask, self.position.exposure)
        # Check pips
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("0.00137"))
        # Check profit base
        profit_base = self.position.calculate_profit_base(self.position.exposure)
        self.assertEqual(profit_base, Decimal("1.82077"))
        # Check profit percentage
        profit_perc = self.position.calculate_profit_perc(self.position.exposure)
        self.assertEqual(profit_perc, Decimal("0.09104"))


class TestShortGBPUSDPosition(unittest.TestCase):
    def setUp(self):
        getcontext.prec = 2
        position_type = "short"
        market = "GBP/USD"
        units = Decimal("2000")
        exposure = Decimal("2000.00")
        bid = Decimal("1.50328")
        ask = Decimal("1.50349")
        self.position = Position(
            position_type, market, 
            units, exposure, bid, ask
        )

    def test_calculate_init_pips(self):
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("-0.00021"))

    def test_calculate_init_profit_base(self):
        profit_base = self.position.calculate_profit_base(self.position.exposure)
        self.assertEqual(profit_base, Decimal("-0.27935"))

    def test_calculate_init_profit_perc(self):
        profit_perc = self.position.calculate_profit_perc(self.position.exposure)
        self.assertEqual(profit_perc, Decimal("-0.01397"))

    def test_calculate_updated_values(self):
        """
        Check that after the bid/ask prices move, that the updated
        pips, profit and percentage profit calculations are correct.
        """
        bid = Decimal("1.50486")
        ask = Decimal("1.50586")
        self.position.update_position_price(bid, ask, self.position.exposure)
        # Check pips
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("-0.00258"))
        # Check profit base
        profit_base = self.position.calculate_profit_base(self.position.exposure)
        self.assertEqual(profit_base, Decimal("-3.42661"))
        # Check profit percentage
        profit_perc = self.position.calculate_profit_perc(self.position.exposure)
        self.assertEqual(profit_perc, Decimal("-0.17133"))


if __name__ == "__main__":
    unittest.main()