# CRON_TO_RUN_EVERY_DAY_1_AM = '0 1 * * *'
from utils import get_itrs_path, get_quotes_path
from main import load_itr
import download
import datetime
import pandas as pd
import yfinance as yf

end_date = datetime.date.today()
start_date = str(datetime.date.today() - datetime.timedelta(days=1)).split(' ')[0]

def fix_date(date):
  return str(date).split(' ')[0]

def get_quotes():
  download.download_itrs(str(end_date.year)) # download fresh new itrs
  df = load_itr(get_itrs_path())
  new_df_quotes = pd.DataFrame()

  for ticker in df['TICKER'].unique():
    ticker_yf = f'{ticker}.SA'
    data = yf.download(tickers=ticker_yf, interval='1d', start=start_date, end=end_date).reset_index()
    data['TICKER'] = ticker
    new_df_quotes = new_df_quotes.append(data)

  new_df_quotes = new_df_quotes[['Date', 'TICKER', 'Adj Close', 'Volume']]
  new_df_quotes = new_df_quotes.dropna()
  new_df_quotes = new_df_quotes[new_df_quotes['Date'] == start_date]
  new_df_quotes['Date'] = new_df_quotes['Date'].apply(fix_date)

  # TODO: Change to save on mongo
  path = get_quotes_path()
  try:
    df_quotes = pd.read_csv(path)
    df_quotes = df_quotes.append(new_df_quotes)
    df_quotes.to_csv(path, index=False)
  except FileNotFoundError:
    new_df_quotes.to_csv(path, index=False)

if __name__ == '__main__':
    get_quotes()
