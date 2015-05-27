from __future__ import print_function

import calendar
import copy
import datetime
import os, os.path
import sys

import numpy as np
import pandas as pd

from qsforex import settings


def month_weekdays(year_int, month_int):
    """
    Produces a list of datetime.date objects representing the
    weekdays in a particular month, given a year.
    """
    cal = calendar.Calendar()
    return [
        d for d in cal.itermonthdates(year_int, month_int) 
        if d.weekday() < 5 and d.year == year_int
    ]


if __name__ == "__main__":
    try:
        pair = sys.argv[1]
    except IndexError:
        print("You need to enter a currency pair, e.g. GBPUSD, as a command line parameter.")
    else:
        np.random.seed(42)  # Fix the randomness

        S0 = 1.5000
        spread = 0.002
        mu_dt = 1400  # Milliseconds
        sigma_dt = 100  # Millseconds
        ask = copy.deepcopy(S0) + spread / 2.0
        bid = copy.deepcopy(S0) - spread / 2.0
        days = month_weekdays(2014, 1)  # January 2014
        current_time = datetime.datetime(
            days[0].year, days[0].month, days[0].day, 0, 0, 0,
        )

        # Loop over every day in the month and create a CSV file
        # for each day, e.g. "GBPUSD_20150101.csv"
        for d in days:
            print(d.day)
            current_time = current_time.replace(day=d.day)
            outfile = open(
                os.path.join(
                    settings.CSV_DATA_DIR, 
                    "%s_%s.csv" % (
                        pair, d.strftime("%Y%m%d")
                    )
                ), 
            "w")
            outfile.write("Time,Ask,Bid,AskVolume,BidVolume\n")     
            
            # Create the random walk for the bid/ask prices
            # with fixed spread between them
            while True:
                dt = abs(np.random.normal(mu_dt, sigma_dt))
                current_time += datetime.timedelta(0, 0, 0, dt)
                if current_time.day != d.day:
                    outfile.close()
                    break
                else:
                    W = np.random.standard_normal() * dt / 1000.0 / 86400.0
                    ask += W
                    bid += W
                    ask_volume = 1.0 + np.random.uniform(0.0, 2.0)
                    bid_volume = 1.0 + np.random.uniform(0.0, 2.0)
                    line = "%s,%s,%s,%s,%s\n" % (
                        current_time.strftime("%d.%m.%Y %H:%M:%S.%f")[:-3], 
                        "%0.5f" % ask, "%0.5f" % bid,
                        "%0.2f00" % ask_volume, "%0.2f00" % bid_volume
                    )
                    outfile.write(line)
