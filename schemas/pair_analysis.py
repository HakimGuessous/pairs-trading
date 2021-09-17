from pydantic import BaseModel
import pandas as pd

class pair_stats(BaseModel):
    ticker1_mean_std_p1: float
    ticker1_mean_std_n1: float
    ticker1_mean_diff: float
    ticker2_mean_std_p1: float
    ticker2_mean_std_n1: float
    ticker2_mean_diff: float
    no_long_signals: int
    no_short_signals: int
    return_all: float
    return_long: float
    return_short: float
    time_in_market_all: pd.Timedelta
    time_in_market_long: pd.Timedelta
    time_in_market_short: pd.Timedelta

    def encode(self):
        return vars(self)
