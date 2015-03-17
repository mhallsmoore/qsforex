# QuantStart Forex

QSForex is an open-source work-in-progress event-driven backtesting and live trading platform for use in the foreign exchange ("forex") markets. 

It has been created as part of the Forex Trading Diary series on QuantStart.com, predominantly for education purposes, but also to provide the systematic trading community with a robust trading engine that allows straightforward forex strategy implementation and testing. 

The software is provided under a permissive "MIT" license (see below).

# Current Features

* Currently in alpha mode - very early stage!
* Live trading with one particular forex broker, OANDA, via their Rest API
* Event-driven architecture with price streaming (via the OANDA API)
* Basic local portfolio replication of live trades (ultimately for backtesting purposes)

# Installation and Usage

At this stage, since the software is in alpha mode, the installation instructions are somewhat more involved. As the software evolves they will become more straightforward and documentation will become more extensive. However, the basic approach is as follows:

1. Setup an account with OANDA and obtain the API authentication credentials
2. Clone the repository into a suitable location on your machine
3. Create two environment variables: OANDA_API_ACCESS_TOKEN and OANDA_API_ACCOUNT_ID, which must contain, respectively, the OANDA API Access Token and the OANDA API Account ID, as provided by OANDA
4. Create a virtual environment ("virtualenv") for the QSForex code and utilise pip to install the requirements - `pip install -r requirements.txt`
5. Modify `strategy.py` to create an event-driven strategy class
6. Execute `trading.py` to carry out practice/live trading

If you have any questions about the installation then please feel free to email me at mike AT quantstart DOT com. You might also wish to have a look at the Forex Trading Diary series on QuantStart in order to gain some intuition about how the system is built.

# License Terms

Copyright (c) 2015 Michael Halls-Moore

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Forex Trading Disclaimer

Trading foreign exchange on margin carries a high level of risk, and may not be suitable for all investors. Past performance is not indicative of future results. The high degree of leverage can work against you as well as for you. Before deciding to invest in foreign exchange you should carefully consider your investment objectives, level of experience, and risk appetite. The possibility exists that you could sustain a loss of some or all of your initial investment and therefore you should not invest money that you cannot afford to lose. You should be aware of all the risks associated with foreign exchange trading, and seek advice from an independent financial advisor if you have any doubts.