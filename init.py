# RUN THIS FILE IF YOU JUST CLONED THE REPO. THIS WILL:
# 1 - CREATE THE ACCOUNTS DICTIONARY
# 2 - DOWNLOAD ALL THE QUOTES FROM 2015 UNTIL NOW
# 3 - PROCESS THE INDICATORS TO ALL COMPANIES
import datetime
from utils import get_itrs_path, get_quotes_path
import pandas as pd
import yfinance as yf
from download import download_itrs
from main import load_itr, process
from generate_accounts import download_account_dictionary

def fix_date(date):
  return str(date).split(' ')[0]

def get_quotes_from_dates(start_date, end_date):
  download_itrs(str(end_date.year))
  df = load_itr()
  new_df_quotes = pd.DataFrame()

  for ticker in df['TICKER'].unique():
    ticker_yf = f'{ticker}.SA'
    data = yf.download(tickers=ticker_yf, interval='1d', start=start_date, end=end_date).reset_index()
    data['TICKER'] = ticker
    new_df_quotes = new_df_quotes.append(data)

  new_df_quotes = new_df_quotes[['Date', 'TICKER', 'Adj Close', 'Volume']]
  new_df_quotes = new_df_quotes.dropna()
  new_df_quotes['Date'] = new_df_quotes['Date'].apply(fix_date)

  path = get_quotes_path()
  try:
    df_quotes = pd.read_csv(path)
    df_quotes = df_quotes.append(new_df_quotes)
    df_quotes.to_csv(path, index=False)
  except FileNotFoundError:
    new_df_quotes.to_csv(path, index=False)


def init():
  # print('Downloading account dictionary...')
  # first_year = 2015
  # current_year = datetime.datetime.now().year
  # years = [first_year]

  # while (len(years) < (current_year - first_year + 1)):
  #   years.append((years[-1] + 1))
  
  # # download_account_dictionary()
  # print(f'Start downloading quotes from {years[0]} to {years[-1]}')
  # for year in years:
  #   start_date = datetime.datetime.now().date().replace(year=year - 1, month=12, day=31)
  #   end_date = datetime.datetime.now().date().replace(year=year, month=12, day=31)
  #   get_quotes_from_dates(start_date, end_date)
  print('Download quotes finished')
  process()


if __name__ == "__main__":
  init()
