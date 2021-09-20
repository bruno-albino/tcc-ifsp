# CRON JOB TO RUN EVERY YEAR
from main import load_itr
import download
from datetime import date
import pandas as pd

data_atual = date.today().year

def download_account_dictionary():
  download.download_itrs(str(data_atual))
  df = load_itr('./itrs')

  # Extract account names
  accounts = df[['CD_CONTA', 'DS_CONTA']].copy()
  accounts['DS_CONTA'] = accounts['DS_CONTA'].str.lower()
  accounts['DS_CONTA'] = accounts['DS_CONTA']\
      .str.normalize('NFKD')\
      .str.encode('ascii', errors='ignore')\
      .str.decode('utf-8')
  accounts = accounts.sort_values('CD_CONTA')
  accounts = accounts.drop_duplicates(keep='first', ignore_index=True)
  df = pd.DataFrame(accounts)
  df.set_index('CD_CONTA', inplace=True)
  df.to_csv('./data/processed/accounts.csv')
