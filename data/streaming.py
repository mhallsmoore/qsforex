from decimal import Decimal, ROUND_HALF_DOWN
import requests
import json

from qsforex.event.event import TickEvent
from qsforex.data.price import PriceHandler


class StreamingForexPrices(PriceHandler):
    def __init__(
        self, domain, access_token, 
        account_id, pairs, events_queue
    ):
        self.domain = domain
        self.access_token = access_token
        self.account_id = account_id
        self.events_queue = events_queue
        self.pairs = pairs
        self.prices = self._set_up_prices_dict()

    def invert_prices(self, pair, bid, ask):
        """
        Simply inverts the prices for a particular currency pair.
        This will turn the bid/ask of "GBPUSD" into bid/ask for
        "USDGBP" and place them in the prices dictionary.
        """
        inv_pair = "%s%s" % (pair[3:], pair[:3])
        inv_bid = (Decimal("1.0")/bid).quantize(
            Decimal("0.00001", ROUND_HALF_DOWN)
        )
        inv_ask = (Decimal("1.0")/ask).quantize(
            Decimal("0.00001", ROUND_HALF_DOWN)
        )
        return inv_pair, inv_bid, inv_ask

    def connect_to_stream(self):
        pairs_oanda = ["%s_%s" % (p[:3], p[3:]) for p in self.pairs]
        try:
            s = requests.Session()
            url = "https://" + self.domain + "/v1/prices"
            headers = {'Authorization' : 'Bearer ' + self.access_token}
            params = {'instruments' : pairs_oanda, 'accountId' : self.account_id}
            req = requests.Request('GET', url, headers=headers, params=params)
            pre = req.prepare()
            resp = s.send(pre, stream=True, verify=False)
            return resp
        except Exception as e:
            s.close()
            print "Caught exception when connecting to stream\n" + str(e) 

    def stream_to_queue(self):
        response = self.connect_to_stream()
        if response.status_code != 200:
            return
        for line in response.iter_lines(1):
            if line:
                try:
                    msg = json.loads(line)
                except Exception as e:
                    print "Caught exception when converting message into json\n" + str(e)
                    return
                if msg.has_key("instrument") or msg.has_key("tick"):
                    print msg
                    instrument = msg["tick"]["instrument"].replace("_", "")
                    time = msg["tick"]["time"]
                    bid = Decimal(str(msg["tick"]["bid"])).quantize(
                        Decimal("0.00001", ROUND_HALF_DOWN)
                    )
                    ask = Decimal(str(msg["tick"]["ask"])).quantize(
                        Decimal("0.00001", ROUND_HALF_DOWN)
                    )
                    self.prices[instrument]["bid"] = bid
                    self.prices[instrument]["ask"] = ask
                    # Invert the prices (GBP_USD -> USD_GBP)
                    inv_pair, inv_bid, inv_ask = self.invert_prices(instrument, bid, ask)
                    self.prices[inv_pair]["bid"] = inv_bid
                    self.prices[inv_pair]["ask"] = inv_ask
                    self.prices[inv_pair]["time"] = time
                    tev = TickEvent(instrument, time, bid, ask)
                    self.events_queue.put(tev)
