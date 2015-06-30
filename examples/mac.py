from __future__ import print_function

from qsforex.backtest.backtest import Backtest
from qsforex.execution.execution import SimulatedExecution
from qsforex.portfolio.portfolio import Portfolio
from qsforex import settings
from qsforex.strategy.strategy import MovingAverageCrossStrategy
from qsforex.data.price import HistoricCSVPriceHandler


if __name__ == "__main__":
    # Trade on GBP/USD and EUR/USD
    pairs = ["GBPUSD", "EURUSD"]
    
    # Create the strategy parameters for the
    # MovingAverageCrossStrategy
    strategy_params = {
        "short_window": 500, 
        "long_window": 2000
    }
   
    # Create and execute the backtest
    backtest = Backtest(
        pairs, HistoricCSVPriceHandler, 
        MovingAverageCrossStrategy, strategy_params, 
        Portfolio, SimulatedExecution, 
        equity=settings.EQUITY
    )
    backtest.simulate_trading()