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

CSV_DATA_DIR = os.environ.get('QSFOREX_CSV_DATA_DIR', None)
OUTPUT_RESULTS_DIR = os.environ.get('QSFOREX_OUTPUT_RESULTS_DIR', None)

DOMAIN = "practice"
STREAM_DOMAIN = ENVIRONMENTS["streaming"][DOMAIN]
API_DOMAIN = ENVIRONMENTS["api"][DOMAIN]
ACCESS_TOKEN = os.environ.get('OANDA_API_ACCESS_TOKEN', None)
ACCOUNT_ID = os.environ.get('OANDA_API_ACCOUNT_ID', None)

BASE_CURRENCY = "GBP"
EQUITY = Decimal("100000.00")
