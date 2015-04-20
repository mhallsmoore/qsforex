from decimal import Decimal
import os
import logging

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

DOMAIN = "practice"
STREAM_DOMAIN = ENVIRONMENTS["streaming"][DOMAIN]
API_DOMAIN = ENVIRONMENTS["api"][DOMAIN]
ACCESS_TOKEN = os.environ.get('OANDA_API_ACCESS_TOKEN', None)
ACCOUNT_ID = os.environ.get('OANDA_API_ACCOUNT_ID', None)

BASE_CURRENCY = "GBP"
EQUITY = Decimal("100000.00")

logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

fh = logging.FileHandler("backtest.log");
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

logger.debug('testowy debug')
logger.info('testowe info')
