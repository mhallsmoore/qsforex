# QuantStart Forex

QSForex is an open-source event-driven backtesting and live trading platform for use in the foreign exchange ("forex") markets, currently in an "alpha" state.

It has been created as part of the Forex Trading Diary series on QuantStart.com to provide the systematic trading community with a robust trading engine that allows straightforward forex strategy implementation and testing. 

The software is provided under a permissive "MIT" license (see below).

# Current Features

* **Open-Source** - QSForex has been released under an extremely permissive open-source MIT License, which allows full usage in both research and commercial applications, without restriction, but with no warranty of any kind whatsoever.
* **Free** - QSForex is completely free and costs nothing to download or use.
* **Collaboration** - As QSForex is open-source many developers collaborate to improve the software. New features are added frequently. Any bugs are quickly determined and fixed.
* **Software Development** - QSForex is written in the Python programming language for straightforward cross-platform support. QSForex contains a suite of unit tests for the majority of its calculation code and new tests are constantly added for new features.</li>
* **Event-Driven Architecture** - QSForex is completely event-driven both for backtesting and live trading, which leads to straightforward transitioning of strategies from a research/testing phase to a live trading implementation.
* **Transaction Costs** - Spread costs are included by default for all backtested strategies.
* **Backtesting** - QSForex features intraday tick-resolution multi-day multi-currency pair backtesting.
* **Trading** - QSForex currently supports live intraday trading using the OANDA Brokerage API across a portfolio of pairs.
* **Performance Metrics** - QSForex currently supports basic performance measurement and equity visualisation via the Matplotlib and Seaborn visualisation libraries.

# Installation and Usage

1) Visit http://www.oanda.com/ and setup an account to obtain the API authentication credentials, which you will need to carry out live trading. I explain how to carry this out in this article: https://www.quantstart.com/articles/Forex-Trading-Diary-1-Automated-Forex-Trading-with-the-OANDA-API.

2) Clone this git repository into a suitable location on your machine using the following command in your terminal: ```git clone https://github.com/mhallsmoore/qsforex.git```. Alternative you can download the zip file of the current master branch at https://github.com/mhallsmoore/qsforex/archive/master.zip.

3) Create a set of environment variables for all of the settings found in the ```settings.py``` file in the application root directory. Alternatively, you can "hard code" your specific settings by overwriting the ```os.environ.get(...)``` calls for each setting:

```
# The data directory used to store your backtesting CSV files
CSV_DATA_DIR = "/path/to/your/csv/data/dir"

# The directory where the backtest.csv and equity.csv files 
# will be stored after a backtest is carried out
OUTPUT_RESULTS_DIR = "/path/to/your/output/results/dir"

# Change DOMAIN to "real" if you wish to carry out live trading
DOMAIN = "practice"

# Your OANDA API Access Token (found in your Account Details on their website)
ACCESS_TOKEN = "1234123412341234"

# Your OANDA Account ID (found in your Account Details on their website)
ACCOUNT_ID = "1234123412341234"

# Your base currency (e.g. "GBP", "USD", "EUR" etc.)
BASE_CURRENCY = "GBP"

# Your account equity in the base currency (for backtesting)
EQUITY = Decimal("100000.00")
```

4) Create a virtual environment ("virtualenv") for the QSForex code and utilise pip to install the requirements. For instance in a Unix-based system (Mac or Linux) you might create such a directory as follows by entering the following commands in the terminal:

```
mkdir -p ~/venv/qsforex
cd ~/venv/qsforex
virtualenv .
```

This will create a new virtual environment to install the packages into. Assuming you downloaded the QSForex git repository into an example directory such as ```~/projects/qsforex/``` (change this directory below to wherever you installed QSForex), then in order to install the packages you will need to run the following commands:

```
source ~/venv/qsforex/bin/activate
pip install -r ~/projects/qsforex/requirements.txt
```

This will take some time as NumPy, SciPy, Pandas, Scikit-Learn and Matplotlib must be compiled. There are many packages required for this to work, so please take a look at these two articles for more information:

* https://www.quantstart.com/articles/Quick-Start-Python-Quantitative-Research-Environment-on-Ubuntu-14-04
* https://www.quantstart.com/articles/Easy-Multi-Platform-Installation-of-a-Scientific-Python-Stack-Using-Anaconda

You will also need to create a symbolic link from your ```site-packages``` directory to your QSForex installation directory in order to be able to call ```import qsforex``` within the code. To do this you will need a command similar to the following:

```
ln -s ~/projects/qsforex/ ~/venv/qsforex/lib/python2.7/site-packages/qsforex
```

Make sure to change ```~/projects/qsforex``` to your installation directory and ```~/venv/qsforex/lib/python2.7/site-packages/``` to your virtualenv site packages directory.

You will now be able to run the subsequent commands correctly.

## Practice/Live Trading

5) At this stage, if you simply wish to carry out practice or live trading then you can run ```python trading/trading.py```, which will use the default ```TestStrategy``` trading strategy. This simply buys or sells a currency pair every 5th tick. It is purely for testing - do not use it in a live trading environment!

If you wish to create a more useful strategy, then simply create a new class with a descriptive name, e.g. ```MeanReversionMultiPairStrategy``` and ensure it has a ```calculate_signals``` method. You will need to pass this class the ```pairs``` list as well as the ```events``` queue, as in ```trading/trading.py```.

Please look at ```strategy/strategy.py``` for details.

## Backtesting

6) In order to carry out any backtesting it is necessary to generate simulated forex data or download historic tick data. If you wish to simply try the software out, the quickest way to generate an example backtest is to generate some simulated data. The current data format used by QSForex is the same as that provided by the DukasCopy Historical Data Feed at https://www.dukascopy.com/swiss/english/marketwatch/historical/.

To generate some historical data, make sure that the ```CSV_DATA_DIR``` setting in ```settings.py``` is to set to a directory where you want the historical data to live. You then need to run ```generate_simulated_pair.py```, which is under the ```scripts/``` directory. It expects a single command line argument, which in this case is the currency pair in ```BBBQQQ``` format. For example:

```
cd ~/projects/qsforex
python scripts/generate_simulated_pair.py GBPUSD
```

At this stage the script is hardcoded to create a single month's data for January 2014. That is, you will see individual files, of the format ```BBBQQQ_YYYYMMDD.csv``` (e.g. ```GBPUSD_20140112.csv```) appear in your ```CSV_DATA_DIR``` for all business days in that month. If you wish to change the month/year of the data output, simply modify the file and re-run.

7) Now that the historical data has been generated it is possible to carry out a backtest. The backtest file itself is stored in ```backtest/backtest.py```, but this only contains the ```Backtest``` class. To actually execute a backtest you need to instantiate this class and provide it with the necessary modules. 

The best way to see how this is done is to look at the example Moving Average Crossover implementation in the ```examples/mac.py``` file and use this as a template. This makes use of the ```MovingAverageCrossStrategy``` which is found in ```strategy/strategy.py```. This defaults to trading both GBP/USD and EUR/USD to demonstrate multiple currency pair usage. It uses data found in ```CSV_DATA_DIR```.

To execute the example backtest, simply run the following:

```
python examples/mac.py
```

**This will take some time.** On my Ubuntu desktop system at home, with the historical data generated via ```generate_simulated_pair.py```, it takes around 5-10 mins to run. A large part of this calculation occurs at the end of the actual backtest, when the drawdown is being calculated, so please remember that the code has not hung up! Please leave it until completion.

8) If you wish to view the performance of the backtest you can simply use ```output.py``` to view an equity curve, period returns (i.e. tick-to-tick returns) and a drawdown curve:

```
python backtest/output.py
```

And that's it! At this stage you are ready to begin creating your own backtests by modifying or appending strategies in ```strategy/strategy.py``` and using real data downloaded from DukasCopy (https://www.dukascopy.com/swiss/english/marketwatch/historical/).

If you have any questions about the installation then please feel free to email me at mike@quantstart.com.

If you have any bugs or other issues that you think may be due to the codebase specifically, feel free to open a Github issue here: https://github.com/mhallsmoore/qsforex/issues

# License Terms

Copyright (c) 2015 Michael Halls-Moore

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Forex Trading Disclaimer

Trading foreign exchange on margin carries a high level of risk, and may not be suitable for all investors. Past performance is not indicative of future results. The high degree of leverage can work against you as well as for you. Before deciding to invest in foreign exchange you should carefully consider your investment objectives, level of experience, and risk appetite. The possibility exists that you could sustain a loss of some or all of your initial investment and therefore you should not invest money that you cannot afford to lose. You should be aware of all the risks associated with foreign exchange trading, and seek advice from an independent financial advisor if you have any doubts.