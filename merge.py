import pandas as pd
from teste import get_quotes_df
from tqdm import tqdm
from pathlib import Path

dir = Path('./data/processed')

def merge_processed():
  df = pd.DataFrame()
  files_to_read = [f for f in list(dir.glob('processed*.csv'))]

  for file in tqdm(files_to_read, dynamic_ncols=True):
    df = df.append(pd.read_csv(file))

  df.to_csv('./data/processed/processed.csv')

def merge_indicators():
  df = pd.DataFrame()
  files_to_read = [f for f in list(dir.glob('indicators*.csv'))]

  for file in tqdm(files_to_read, dynamic_ncols=True):
    df = df.append(pd.read_csv(file))

  df.to_csv('./data/processed/indicators.csv')

# def create_full_quotes():
#   df = pd.read_csv('./data/processed/indicators.csv')
#   tickers = df.ticker.unique()
#   df_quotes = get_quotes_df(tickers)['Adj Close']
#   df_quotes.to_csv('./data/processed/quotes.csv')

def merge():
  merge_processed()
  merge_indicators()
  # create_full_quotes()

if __name__ == "__main__":
  merge()
