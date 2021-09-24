import os
from pathlib import Path

def get_itrs_path():
  return './itrs'

def get_itr_names():
  names = ['DVA', 'DRE', 'DRA', 'DMPL', 'DFC_MI', 'BPP', 'BPA']
  return names

def get_quotes_path():
  return './data/processed/quotes.csv'

def get_processed_path():
  return './data/processed/processed.csv'

def get_indicators_path():
  return './data/processed/indicators.csv'

def get_download_path():
  return './data/downloaded'

def get_chromedriver_path():
  value = os.path.join(Path(__file__).parent.resolve(), 'chrome-drivers')
  return value

