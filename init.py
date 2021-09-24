# RUN THIS FILE IF YOU JUST CLONED THE REPO. THIS WILL:
# 1 - CREATE THE ACCOUNTS DICTIONARY
# 2 - DOWNLOAD ALL THE QUOTES FROM 2015 UNTIL NOW
# 3 - PROCESS THE INDICATORS TO ALL COMPANIES

import datetime
import pandas as pd
import yfinance as yf
from utils import get_quotes_path
from download import download_instrument_consolidated, download_itrs
from main import load_itr, process
from generate_accounts import download_account_dictionary

quotes_path = get_quotes_path()

def fix_date(date):
  return str(date).split(' ')[0]

def get_remaining_quotes():
  df_quotes = pd.read_csv(quotes_path)

  # get last quote date
  date = df_quotes['Date'].max()
  [year, month, day] = date.split('-')
  
  start_date = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(days=1)
  end_date = datetime.date.today()

  print(f'Quotes exists. Downloading remaining quotes from {start_date} to {end_date}')
  new_df_quotes = get_quotes_from_dates(start_date, end_date)
  
  df_quotes = df_quotes.append(new_df_quotes)
  df_quotes.to_csv(quotes_path, index=False)

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

  return new_df_quotes

def generate_fresh_quotes():
  first_year = 2015
  current_year = datetime.datetime.now().year
  years = [first_year]

  while (len(years) < (current_year - first_year + 1)):
    years.append((years[-1] + 1))
  
  print('Quotes don\'t exist. Downloading fresh quotes from {years[0]}x to {years[-1]}')
  df = pd.DataFrame()

  for year in years:
    start_date = datetime.datetime.now().date().replace(year=year - 1, month=12, day=31)
    end_date = datetime.datetime.now().date().replace(year=year, month=12, day=31)
    df_quotes = get_quotes_from_dates(start_date, end_date)
    df = df.append(df_quotes)

  df.to_csv(quotes_path, index=False)
  print('Download fresh quotes finished')

def init():
  print('Downloading instrument consolidated file...')
  download_instrument_consolidated()

  print('Downloading account dictionary...')
  download_account_dictionary()

  # check if quotes exists
  try:
    pd.read_csv(quotes_path)
    get_remaining_quotes()
  except FileNotFoundError:
    # file don´t exists, create 
    generate_fresh_quotes()

  download_itrs('2021')
  process()


if __name__ == "__main__":
  init()
