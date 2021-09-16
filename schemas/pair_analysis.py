from pydantic import BaseModel


class pair_stats(BaseModel):
    ticker1_mean_std_p1: float
    ticker1_mean_std_n1: float
    ticker1_mean_diff: float
    ticker2_mean_std_p1: float
    ticker2_mean_std_n1: float
    ticker2_mean_diff: float
    sdv_cross_per_year: float
