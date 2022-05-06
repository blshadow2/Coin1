from pandas import DataFrame
from sqlite3 import Time
import requests
import pandas as pd
import time
import xmltodict
import datetime
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
def rsi(ohlc: pd.DataFrame, period: int = 14):
    ohlc["trade_price"] = ohlc["trade_price"]
    delta = ohlc["trade_price"].diff()
    gains, declines = delta.copy(), delta.copy()
    gains[gains < 0] = 0
    declines[declines > 0] = 0

    _gain = gains.ewm(com=(period - 1), min_periods=period).mean()
    _loss = declines.abs().ewm(com=(period - 1), min_periods=period).mean()

    RS = _gain / _loss
    return pd.Series(100 - (100 / (1 + RS)), name="RSI")


while True:
    url = "https://api.upbit.com/v1/candles/minutes/1"
    querystring = {"market":"KRW-BTC","count":"200"}
    response = requests.request("GET", url, params=querystring)
    data = response.json()
    df = pd.DataFrame(data)
    df=df.reindex(index=df.index[::-1]).reset_index()
    nrsi = rsi(df, 14).iloc[-1] 
    f = open("Python/txt/rsi.txt", 'w')
    print(nrsi, file=f)
    f.close()
    time.sleep(1)
