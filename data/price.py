from __future__ import print_function

import datetime
from decimal import Decimal, getcontext, ROUND_HALF_DOWN
import os
import os.path
import re
import time

import numpy as np
import pandas as pd

from qsforex import settings
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

    def _set_up_prices_dict(self):
        """
        Due to the way that the Position object handles P&L
        calculation, it is necessary to include values for not
        only base/quote currencies but also their reciprocals.
        This means that this class will contain keys for, e.g.
        "GBPUSD" and "USDGBP".

        At this stage they are calculated in an ad-hoc manner,
        but a future TODO is to modify the following code to
        be more robust and straightforward to follow.
        """
        prices_dict = dict(
            (k, v) for k,v in [
                (p, {"bid": None, "ask": None, "time": None}) for p in self.pairs
            ]
        )
        inv_prices_dict = dict(
            (k, v) for k,v in [
                (
                    "%s%s" % (p[3:], p[:3]), 
                    {"bid": None, "ask": None, "time": None}
                ) for p in self.pairs
            ]
        )
        prices_dict.update(inv_prices_dict)
        return prices_dict

    def invert_prices(self, pair, bid, ask):
        """
        Simply inverts the prices for a particular currency pair.
        This will turn the bid/ask of "GBPUSD" into bid/ask for
        "USDGBP" and place them in the prices dictionary.
        """
        getcontext().rounding = ROUND_HALF_DOWN
        inv_pair = "%s%s" % (pair[3:], pair[:3])
        inv_bid = (Decimal("1.0")/bid).quantize(
            Decimal("0.00001")
        )
        inv_ask = (Decimal("1.0")/ask).quantize(
            Decimal("0.00001")
        )
        return inv_pair, inv_bid, inv_ask


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
        self.prices = self._set_up_prices_dict()
        self.pair_frames = {}
        self.file_dates = self._list_all_file_dates()
        self.continue_backtest = True
        self.cur_date_idx = 0
        self.cur_date_pairs = self._open_convert_csv_files_for_day(
            self.file_dates[self.cur_date_idx]
        )

    def _list_all_csv_files(self):
        files = os.listdir(settings.CSV_DATA_DIR)
        pattern = re.compile("[A-Z]{6}_\d{8}.csv")
        matching_files = [f for f in files if pattern.search(f)]
        matching_files.sort()
        return matching_files

    def _list_all_file_dates(self):
        """
        Removes the pair, underscore and '.csv' from the
        dates and eliminates duplicates. Returns a list
        of date strings of the form "YYYYMMDD". 
        """
        csv_files = self._list_all_csv_files()
        de_dup_csv = list(set([d[7:-4] for d in csv_files]))
        de_dup_csv.sort()
        return de_dup_csv

    def _open_convert_csv_files_for_day(self, date_str):
        """
        Opens the CSV files from the data directory, converting
        them into pandas DataFrames within a pairs dictionary.
        
        The function then concatenates all of the separate pairs
        for a single day into a single data frame that is time 
        ordered, allowing tick data events to be added to the queue 
        in a chronological fashion.
        """
        for p in self.pairs:
            pair_path = os.path.join(self.csv_dir, '%s_%s.csv' % (p, date_str))
            self.pair_frames[p] = pd.io.parsers.read_csv(
                pair_path, header=True, index_col=0, 
                parse_dates=True, dayfirst=True,
                names=("Time", "Ask", "Bid", "AskVolume", "BidVolume")
            )
            self.pair_frames[p]["Pair"] = p
        return pd.concat(self.pair_frames.values()).sort().iterrows()

    def _update_csv_for_day(self):
        try:
            dt = self.file_dates[self.cur_date_idx+1]
        except IndexError:  # End of file dates
            return False
        else:
            self.cur_date_pairs = self._open_convert_csv_files_for_day(dt)
            self.cur_date_idx += 1
            return True

    def stream_next_tick(self):
        """
        The Backtester has now moved over to a single-threaded
        model in order to fully reproduce results on each run.
        This means that the stream_to_queue method is unable to
        be used and a replacement, called stream_next_tick, is
        used instead.

        This method is called by the backtesting function outside
        of this class and places a single tick onto the queue, as
        well as updating the current bid/ask and inverse bid/ask.
        """
        try:
            index, row = next(self.cur_date_pairs)
        except StopIteration:
            # End of the current days data
            if self._update_csv_for_day():
                index, row = next(self.cur_date_pairs)
            else: # End of the data
                self.continue_backtest = False
                return
        
        getcontext().rounding = ROUND_HALF_DOWN
        pair = row["Pair"]
        bid = Decimal(str(row["Bid"])).quantize(
            Decimal("0.00001")
        )
        ask = Decimal(str(row["Ask"])).quantize(
            Decimal("0.00001")
        )

        # Create decimalised prices for traded pair
        self.prices[pair]["bid"] = bid
        self.prices[pair]["ask"] = ask
        self.prices[pair]["time"] = index

        # Create decimalised prices for inverted pair
        inv_pair, inv_bid, inv_ask = self.invert_prices(pair, bid, ask)
        self.prices[inv_pair]["bid"] = inv_bid
        self.prices[inv_pair]["ask"] = inv_ask
        self.prices[inv_pair]["time"] = index

        # Create the tick event for the queue
        tev = TickEvent(pair, index, bid, ask)
        self.events_queue.put(tev)
