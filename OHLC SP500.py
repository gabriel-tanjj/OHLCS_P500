import pandas as pd
#make connecting to HTTP easier
import requests
from bs4 import BeautifulSoup
import yfinance


def get_sp500_ticker():
    res = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    #for parsing data
    soup = BeautifulSoup(res.content,"html")
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))
    tickers = list(df[0].Symbol)
    return tickers

#create new variable
tickers = get_sp500_ticker()

def get_history(ticker, period_start, period_end, granularity ="1d"):
    df = yfinance.Ticker(ticker).history(
        start=period_start,
        end=period_end,
        interval=granularity,
        auto_adjust=True
    )

    df = df.rename(columns={
        "Date": "Date & Time",
        "Open":"Daily Open",
        "High": "Daily High",
        "Low" : "Daily Low",
        "Close": "Daily Close",
        "Volume" : "Daily Volume"
    })
    #auto_adjust to ensure that corporate actions like splits etc are taken into account for
    df = df.drop(columns = ["Dividends", "Stock Splits"])
    #if you want to remove a specific column such as "dividends" and "stock splits"
    input(df)

import pytz
#to fix timezone differences
from datetime import datetime

period_start = datetime(2010,1,1, tzinfo=pytz.utc)
period_end = datetime(2023,1,1, tzinfo=pytz.utc)

print(period_start, period_end)

for ticker in tickers:
    df = get_history(ticker, period_start, period_end)
    print(ticker, df)

