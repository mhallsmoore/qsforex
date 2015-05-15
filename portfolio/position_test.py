from decimal import Decimal
import unittest

from position import Position


class TickerMock(object):
    """
    A mock object that allows a representation of the
    ticker/pricing handler.
    """

    def __init__(self):
        self.pairs = ["GBPUSD", "EURUSD"]
        self.prices = {
            "GBPUSD": {"bid": Decimal("1.50328"), "ask": Decimal("1.50349")},
            "USDGBP": {"bid": Decimal("0.66521"), "ask": Decimal("0.66512")},
            "EURUSD": {"bid": Decimal("1.07832"), "ask": Decimal("1.07847")}
        }



# =====================================
# GBP Home Currency with GBP/USD traded
# =====================================

class TestLongGBPUSDPosition(unittest.TestCase):
    """
    Unit tests that cover going long GBP/USD with an account
    denominated currency of GBP, using 2,000 units of GBP/USD.
    """
    def setUp(self):
        home_currency = "GBP"
        position_type = "long"
        currency_pair = "GBPUSD"
        units = Decimal("2000")
        ticker = TickerMock()
        self.position = Position(
            home_currency, position_type, 
            currency_pair, units, ticker
        )

    def test_calculate_init_pips(self):
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("-0.00021"))

    def test_calculate_init_profit_base(self):
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("-0.27939"))

    def test_calculate_init_profit_perc(self):
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("-0.01397"))

    def test_calculate_updated_values(self):
        """
        Check that after the bid/ask prices move, that the updated
        pips, profit and percentage profit calculations are correct.
        """
        prices = self.position.ticker.prices
        prices["GBPUSD"] = {"bid": Decimal("1.50486"), "ask": Decimal("1.50586")}
        prices["USDGBP"] = {"bid": Decimal("0.66451"), "ask": Decimal("0.66407")}
        self.position.update_position_price()

        # Check pips
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("0.00137"))
        # Check profit base
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("1.82076"))
        # Check profit percentage
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("0.09104"))


class TestShortGBPUSDPosition(unittest.TestCase):
    """
    Unit tests that cover going short GBP/USD with an account
    denominated currency of GBP, using 2,000 units of GBP/USD.
    """
    def setUp(self):
        home_currency = "GBP"
        position_type = "short"
        currency_pair = "GBPUSD"
        units = Decimal("2000")
        ticker = TickerMock()
        self.position = Position(
            home_currency, position_type, 
            currency_pair, units, ticker
        )

    def test_calculate_init_pips(self):
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("-0.00021"))

    def test_calculate_init_profit_base(self):
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("-0.27935"))

    def test_calculate_init_profit_perc(self):
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("-0.01397"))

    def test_calculate_updated_values(self):
        """
        Check that after the bid/ask prices move, that the updated
        pips, profit and percentage profit calculations are correct.
        """
        prices = self.position.ticker.prices
        prices["GBPUSD"] = {"bid": Decimal("1.50486"), "ask": Decimal("1.50586")}
        prices["USDGBP"] = {"bid": Decimal("0.66451"), "ask": Decimal("0.66407")}
        self.position.update_position_price()

        # Check pips
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("-0.00258"))
        # Check profit base
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("-3.42660"))
        # Check profit percentage
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("-0.17133"))


# =====================================
# GBP Home Currency with EUR/USD traded
# =====================================

class TestLongEURUSDPosition(unittest.TestCase):
    """
    Unit tests that cover going long EUR/USD with an account
    denominated currency of GBP, using 2,000 units of EUR/USD.
    """
    def setUp(self):
        home_currency = "GBP"
        position_type = "long"
        currency_pair = "EURUSD"
        units = Decimal("2000")
        ticker = TickerMock()
        self.position = Position(
            home_currency, position_type, 
            currency_pair, units, ticker
        )

    def test_calculate_init_pips(self):
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("-0.00015"))

    def test_calculate_init_profit_base(self):
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("-0.19956"))

    def test_calculate_init_profit_perc(self):
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("-0.00998"))

    def test_calculate_updated_values(self):
        """
        Check that after the bid/ask prices move, that the updated
        pips, profit and percentage profit calculations are correct.
        """
        prices = self.position.ticker.prices
        prices["GBPUSD"] = {"bid": Decimal("1.50486"), "ask": Decimal("1.50586")}
        prices["USDGBP"] = {"bid": Decimal("0.66451"), "ask": Decimal("0.66407")}
        prices["EURUSD"] = {"bid": Decimal("1.07811"), "ask": Decimal("1.07827")}
        self.position.update_position_price()

        # Check pips
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("-0.00036"))
        # Check profit base
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("-0.47845"))
        # Check profit percentage
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("-0.02392"))


class TestLongEURUSDPosition(unittest.TestCase):
    """
    Unit tests that cover going short EUR/USD with an account
    denominated currency of GBP, using 2,000 units of EUR/USD.
    """
    def setUp(self):
        home_currency = "GBP"
        position_type = "short"
        currency_pair = "EURUSD"
        units = Decimal("2000")
        ticker = TickerMock()
        self.position = Position(
            home_currency, position_type, 
            currency_pair, units, ticker
        )

    def test_calculate_init_pips(self):
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("-0.00015"))

    def test_calculate_init_profit_base(self):
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("-0.19954"))

    def test_calculate_init_profit_perc(self):
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("-0.00998"))

    def test_calculate_updated_values(self):
        """
        Check that after the bid/ask prices move, that the updated
        pips, profit and percentage profit calculations are correct.
        """
        prices = self.position.ticker.prices
        prices["GBPUSD"] = {"bid": Decimal("1.50486"), "ask": Decimal("1.50586")}
        prices["USDGBP"] = {"bid": Decimal("0.66451"), "ask": Decimal("0.66407")}
        prices["EURUSD"] = {"bid": Decimal("1.07811"), "ask": Decimal("1.07827")}
        self.position.update_position_price()

        # Check pips
        pos_pips = self.position.calculate_pips()
        self.assertEqual(pos_pips, Decimal("0.00005"))
        # Check profit base
        profit_base = self.position.calculate_profit_base()
        self.assertEqual(profit_base, Decimal("0.06641"))
        # Check profit percentage
        profit_perc = self.position.calculate_profit_perc()
        self.assertEqual(profit_perc, Decimal("0.00332"))


if __name__ == "__main__":
    unittest.main()