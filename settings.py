from decimal import Decimal
import os


ENVIRONMENTS = {
    "streaming": {
        "real": "stream-fxtrade.oanda.com",
        "practice": "stream-fxpractice.oanda.com",
        "sandbox": "stream-sandbox.oanda.com"
    },
    "api": {
        "real": "api-fxtrade.oanda.com",
        "practice": "api-fxpractice.oanda.com",
        "sandbox": "api-sandbox.oanda.com"
    }
}

# The data directory used to store your backtesting CSV files
CSV_DATA_DIR = os.environ.get('QSFOREX_CSV_DATA_DIR', 'csvdata')

# The directory where the backtest.csv and equity.csv files
# will be stored after a backtest is carried out
OUTPUT_RESULTS_DIR = os.environ.get('QSFOREX_OUTPUT_RESULTS_DIR', 'results')

# Change DOMAIN to "real" if you wish to carry out live trading
DOMAIN = os.environ.get('QSFOREX_DOMAIN',"practice")
STREAM_DOMAIN = ENVIRONMENTS["streaming"][DOMAIN]
API_DOMAIN = ENVIRONMENTS["api"][DOMAIN]

# Your OANDA API Access Token (found in your Account Details on their website)
ACCESS_TOKEN = os.environ.get('OANDA_API_ACCESS_TOKEN', 'None')

# Your OANDA Account ID (found in your Account Details on their website)
ACCOUNT_ID = os.environ.get('OANDA_API_ACCOUNT_ID', 'None')

# Your base currency (e.g. "GBP", "USD", "EUR" etc.)
BASE_CURRENCY = os.environ.get('QSFOREX_BASE_CURRENCY', "GBP")

# Your account equity in the base currency (for backtesting)
EQUITY = os.environ.get('QSFOREX_EQUITY', Decimal("100000.00"))
