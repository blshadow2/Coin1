import time
import pyupbit
import datetime
from pandas import DataFrame
from sqlite3 import Time
import requests
import pandas as pd
import time
import xmltodict
import datetime
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta



access = "oH7ApFNBJsv8ww9xMTLzPWZtNvQVnHRx473jngAK"          # 본인 값으로 변경
secret = "N3QlyUxNTqK6ddraCe3F5GvNqIfJhIJqj3QteKxs"



def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_rsi():
    "rsi 불러오기" 
    f= open("Python/txt/rsi.txt", encoding='UTF-8')
    rsi = f.readline()
    return rsi


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        rsi = get_rsi()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)
        
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.5)
            ma15 = get_ma15("KRW-BTC")
            current_price = get_current_price("KRW-BTC")
            if rsi<40:
                if target_price < current_price and ma15 < current_price:
                    krw = get_balance("KRW")
                    if krw > 5000:
                        upbit.buy_market_order("KRW-BTC", krw*0.9995)
        
        btc = get_balance("BTC")
        if  btc*target_price < btc*current_price:
            if 60 < rsi:
                if btc > 0.000099:
                    upbit.sell_market_order("KRW-BTC", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)


        