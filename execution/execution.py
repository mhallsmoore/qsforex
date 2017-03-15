from __future__ import print_function

from abc import ABCMeta, abstractmethod
try:
    import httplib
except ImportError:
    import http.client as httplib
import logging
from oandapyV20.contrib.requests import MarketOrderRequest
import oandapyV20.endpoints.orders as orders
import oandapyV20
import json



class ExecutionHandler(object):
    """
    Provides an abstract base class to handle all execution in the
    backtesting and live trading system.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_order(self):
        """
        Send the order to the brokerage.
        """
        raise NotImplementedError("Should implement execute_order()")


class SimulatedExecution(object):
    """
    Provides a simulated execution handling environment. This class
    actually does nothing - it simply receives an order to execute.

    Instead, the Portfolio object actually provides fill handling.
    This will be modified in later versions.
    """
    def execute_order(self, event):
        pass


class OANDAExecutionHandler(ExecutionHandler):
    def __init__(self, domain, access_token, account_id):
        self.domain = domain
        self.access_token = access_token
        self.account_id = account_id
        self.conn = self.obtain_connection()
        self.logger = logging.getLogger(__name__)

    def obtain_connection(self):
        return httplib.HTTPSConnection(self.domain)

    def execute_order(self, event):
        instrument = "%s_%s" % (event.instrument[:3], event.instrument[3:])
        if event.order_type == 'market':
            if event.side == 'buy':
                mktOrder = MarketOrderRequest(
                    instrument=instrument,
                    units= event.units,
                    #type= event.order_type,
                    #side= event.side
                    )
            if event.side == 'sell':
                mktOrder = MarketOrderRequest(
                    instrument=instrument,
                    units= (event.units*-1),
                    #type= event.order_type,
                    #side= event.side
                    )
        else:
            Print('Order Type Not Supported ' + self.order_type)
            return

        accountID = self.account_id
        access_token = self.access_token

        api = oandapyV20.API(access_token=access_token)

        r = orders.OrderCreate(accountID, data=mktOrder.data)
        try:
            #Try and execute order
            rv = api.request(r)
        except oandapyV20.exceptions.V20Error as err:
            print(r.status_code, err)
        else:
            print(json.dumps(rv, indent=2))

        #response = self.conn.getresponse().read().decode("utf-8").replace("\n","").replace("\t","")
        self.logger.debug(json.dumps(rv, indent=2))
        