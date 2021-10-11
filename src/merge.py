import pandas as pd
from tqdm import tqdm
from pathlib import Path

dir = Path('./data/processed')

def merge_processed():
  df = pd.DataFrame()
  files_to_read = [f for f in list(dir.glob('processed-*.csv'))]

  for file in tqdm(files_to_read):
    df = df.append(pd.read_csv(file))

  df.to_csv('./data/processed/processed.csv', index=False)

def merge_indicators():
  df = pd.DataFrame()
  files_to_read = [f for f in list(dir.glob('indicators-*.csv'))]

  for file in tqdm(files_to_read):
    df = df.append(pd.read_csv(file))

  df.to_csv('./data/processed/indicators.csv', index=False)

def merge():
  merge_processed()
  merge_indicators()

if __name__ == "__main__":
  merge()
