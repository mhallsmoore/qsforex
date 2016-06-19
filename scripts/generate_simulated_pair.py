from __future__ import print_function

import click

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

@click.command()
@click.option('--seed', default=42, help='Seed (Fix the randomness by default but use a negative value for true randomness)')
@click.option('--pair', default='GBPUSD', help='Currency pair')
@click.option('--s0', default=1.5000, help='S0')
@click.option('--spread', default=0.002, help='spread')
@click.option('--mu_dt', default=1400, help='mu_dt (Milliseconds)')
@click.option('--sigma_dt', default=100, help='sigma_dt (Milliseconds)')
@click.option('--year', default=2014, help='Year')
@click.option('--month', default=1, help='Month')
def main(seed, pair, s0, spread, mu_dt, sigma_dt, year, month):
    if seed >= 0:
        np.random.seed(seed)

    ask = copy.deepcopy(s0) + spread / 2.0
    bid = copy.deepcopy(s0) - spread / 2.0
    days = month_weekdays(year, month)  # January 2014 by default
    current_time = datetime.datetime(
        days[0].year, days[0].month, days[0].day, 0, 0, 0,
    )

    # Loop over every day in the month and create a CSV file
    # for each day, e.g. "GBPUSD_20150101.csv"
    for d in days:
        current_time = current_time.replace(day=d.day)
        print(d.day)
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

if __name__ == "__main__":
    main()