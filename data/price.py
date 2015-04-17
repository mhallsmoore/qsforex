from abc import ABCMeta, abstractmethod
import datetime
from decimal import Decimal, getcontext, ROUND_HALF_DOWN
import os
import os.path
import numpy as np
import pandas as pd

from qsforex.event.event import TickEvent


class PriceHandler(object):
    """
    PriceHandler is an abstract base class providing an interface for
    all subsequent (inherited) data handlers (both live and historic).

    The goal of a (derived) PriceHandler object is to output a set of
    bid/ask/timestamp "ticks" for each currency pair and place them into
    an event queue.

    This will replicate how a live strategy would function as current
    tick data would be streamed via a brokerage. Thus a historic and live
    system will be treated identically by the rest of the QSForex 
    backtesting suite.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def stream_to_queue(self):
        """
        Streams a sequence of tick data events (timestamp, bid, ask)
        tuples to the events queue.
        """
        raise NotImplementedError("Should implement stream_to_queue()")


class HistoricCSVPriceHandler(PriceHandler):
    """
    HistoricCSVPriceHandler is designed to read CSV files of
    tick data for each requested currency pair and stream those
    to the provided events queue.
    """

    def __init__(self, pairs, events_queue, csv_dir):
        """
        Initialises the historic data handler by requesting
        the location of the CSV files and a list of symbols.

        It will be assumed that all files are of the form
        'pair.csv', where "pair" is the currency pair. For
        GBP/USD the filename is GBPUSD.csv.

        Parameters:
        pairs - The list of currency pairs to obtain.
        events_queue - The events queue to send the ticks to.
        csv_dir - Absolute directory path to the CSV files.
        """
        self.pairs = pairs
        self.events_queue = events_queue
        self.csv_dir = csv_dir
        self.cur_bid = None
        self.cur_ask = None

    def _open_convert_csv_files(self):
        """
        Opens the CSV files from the data directory, converting
        them into pandas DataFrames within a pairs dictionary.
        """
        pair_path = os.path.join(self.csv_dir, '%s.csv' % self.pairs[0])
        self.pair = pd.io.parsers.read_csv(
            pair_path, header=True, index_col=0, parse_dates=True,
            names=("Time", "Ask", "Bid", "AskVolume", "BidVolume")
        ).iterrows()

    def stream_to_queue(self):
        self._open_convert_csv_files()
        for index, row in self.pair:
            self.cur_bid = Decimal(str(row["Bid"])).quantize(
                Decimal("0.00001", ROUND_HALF_DOWN)
            )
            self.cur_ask = Decimal(str(row["Ask"])).quantize(
                Decimal("0.00001", ROUND_HALF_DOWN)
            )
            tev = TickEvent(self.pairs[0], index, row["Bid"], row["Ask"])
            self.events_queue.put(tev)
