import yfinance as yf
from datetime import datetime
import dateutil.relativedelta
import pandas as pd
import numpy as np
from matplotlib import pyplot


class FindPair:
    def __init__(self, ticker1: str, ticker2: str = "SPY", ql: int = 4):
        self.ticker1 = self.get_ticker(ticker1, ql)
        self.ticker2 = self.get_ticker(ticker2, ql)
        self.ticker1_pc = self.ticker1.pct_change()
        self.ticker2_pc = self.ticker2.pct_change()
        self.ticker1_roll = self.ticker1_pc.rolling(60).sum()
        self.ticker2_roll = self.ticker2_pc.rolling(60).sum()
        self.pair_diff = self.ticker1_roll - self.ticker2_roll
        self.pair_mean = self.pair_diff.rolling(240).mean()
        self.pair_std = self.pair_diff.rolling(240).std()
        self.pair_z = (self.pair_diff - self.pair_mean)/self.pair_std
        self.buy_signal = self.find_buy_signal(self.pair_z)
        self.sell_signal = self.find_sell_signal(self.pair_z)

    def get_ticker(self, symbol: str, query_length: int) -> pd.Series:
        date = (datetime.today() - dateutil.relativedelta.relativedelta(years=query_length)).strftime("%Y-%m-%d")
        data = yf.download(symbol, start=date)
        return data.Close

    def find_buy_signal(self, pair_z: pd.Series) -> pd.Series:
        out = []
        state = 0
        for i in pair_z:
            if not -1 < i < 1 and state == 0 and not np.isnan(i):
                out.append(i)
                if -1 > i:
                    state = -1
                else:
                    state = 1
            else:
                out.append(None)
                if state == -1 and i > 0:
                    state = 0
                elif state == 1 and i < 0:
                    state = 0
        return pd.Series(out, index=pair_z.index)

    def find_sell_signal(self, pair_z: pd.Series) -> pd.Series:
        out = []
        state = 0
        for i in pair_z:
            if not -1 < i < 1 and state == 0 and not np.isnan(i):
                out.append(None)
                if -1 > i:
                    state = -1
                else:
                    state = 1
            else:
                if (state == -1 and i > 0) or (state == 1 and i < 0) and not np.isnan(i):
                    out.append(i)
                    state = 0
                else:
                    out.append(None)
        return pd.Series(out, index=pair_z.index)

    def plot_pair(self) -> pyplot.Line2D:
        f, ax = pyplot.subplots()
        ax.plot(self.pair_z)
        ax.scatter(self.buy_signal.index, pair.buy_signal, color = "green")
        ax.scatter(self.sell_signal.index, pair.sell_signal, color="red")
        return ax

    def estimate_results(self):
        pass


pair = FindPair("AMD")
pair.plot_pair()


buy_signals = pair.buy_signal.dropna()
sell_signals = pair.sell_signal.dropna()
all_signals = buy_signals.append(sell_signals).sort_index()
all_prices = pair.ticker1[all_signals.index]
last_price = None
out = []
state = 0
for i in all_signals.index:
    if all_signals[i] < -1:
        last_price = all_prices[i]
        state = 1
    elif all_signals[i] > 1:
        last_price = all_prices[i]
        state = -1
    elif -1 < all_signals[i] < 1 and last_price:
        if state == 1:
            out.append((all_prices[i]/last_price))
        if state == -1:
            #out.append(2-(all_prices[i]/last_price))
            out.append(1)
        state = 0

np.cumprod(out)