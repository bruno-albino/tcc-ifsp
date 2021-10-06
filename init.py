import datetime
import pandas as pd
import yfinance as yf
from utils import get_quotes_path
from download import download_instrument_consolidated, download_itrs
from main import load_itr, process

quotes_path = get_quotes_path()

def fix_date(date):
  return str(date).split(' ')[0]

def get_remaining_quotes():
  df_quotes = pd.read_csv(quotes_path)

  # Busca a data máxima das cotas, e faz o download das cotas restantes
  date = df_quotes['Date'].max()
  [year, month, day] = date.split('-')
  
  start_date = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(days=1)
  end_date = datetime.date.today()

  if start_date.ctime() >= end_date.ctime():
    return

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
  # Gerando arquivo de cotas de 2015 ao ano atual
  first_year = 2015
  current_year = datetime.datetime.now().year
  years = [first_year]

  while (len(years) < (current_year - first_year + 1)):
    years.append((years[-1] + 1))
  
  print(f'Quotes don\'t exist. Downloading fresh quotes from {years[0]}x to {years[-1]}')
  df = pd.DataFrame()

  for year in years:
    start_date = datetime.datetime.now().date().replace(year=year - 1, month=12, day=31)
    end_date = datetime.datetime.now().date().replace(year=year, month=12, day=31)
    df_quotes = get_quotes_from_dates(start_date, end_date)
    df = df.append(df_quotes)

  df.to_csv(quotes_path, index=False)
  print('Download fresh quotes finished')

def init():
  # year = datetime.datetime.today().year

  # Buscar arquivo de cotas, localizado em ./data/processed/quotes.csv
  try:
    pd.read_csv(quotes_path)
    get_remaining_quotes()
  except FileNotFoundError:
    # Arquivo não existe 
    generate_fresh_quotes()

  # for year in ['2021']:
  #   download_itrs(year)
  #   process(year)


if __name__ == "__main__":
  init()
