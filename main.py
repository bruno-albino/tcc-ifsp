from utils import get_download_path, get_itr_names, get_itrs_path, get_processed_path
import numpy as np
import pandas as pd
import process_indicators 
from pathlib import Path
from tqdm import tqdm

def choose_company_tickers(tickers):
    company_tickers = []

    for t in tickers:
        if len(t) == 5 and (t[-1] == '3' or t[-1] == '4'):
            company_tickers.append(t)

    if len(company_tickers) > 0:
        return company_tickers[0]
    else:
        return np.nan

def load_itr():
    itr_names = get_itr_names()
    itr_path = get_itrs_path()
    dir = Path(itr_path)
    df = pd.DataFrame()
    print('Loading data...')

    files_to_read = [f for f in list(dir.glob('itr_cia_aberta_*_*_*.csv'))
                     if any(itr in str(f) for itr in itr_names)]

    for file in tqdm(files_to_read,
                     dynamic_ncols=True):
        df = df.append(pd.read_csv(file, sep=';', encoding='latin1'))

    df = df[df['ORDEM_EXERC'].eq('ÚLTIMO')].reset_index(drop=True)
    df['TICKER'] = df['DENOM_CIA'].apply(name_to_ticker)
    return df


def clean_itr(df):
    temp = df.copy()
    # Drop lines referring to penultimate accounting period, otherwise there
    # would be duplicated values when we load more than one consecutive year.
    temp = temp[temp['ORDEM_EXERC'].eq('ÚLTIMO')].reset_index(drop=True)

    # Remove duplicated rows with different account names
    try:
        temp = temp.sort_values('DT_INI_EXERC')
    except KeyError:
        pass
    temp = temp.groupby(['DT_REFER',
                         'DENOM_CIA',
                        'CD_CONTA']).last().reset_index()

    # Remove unused columns
    temp = temp[['CNPJ_CIA', 'TICKER', 'DT_REFER', 'DENOM_CIA', 'CD_CVM',
                 'CD_CONTA', 'VL_CONTA']]

    # (Hopefully) Remove the remaining duplicated rows
    # temp = temp.drop_duplicates(keep='last', ignore_index=True)

    return temp
dir = Path(get_download_path())
file = [f for f in list(dir.glob('InstrumentsConsolidatedFile*.csv'))][0]
df_b3_instruments = pd.read_csv(file, encoding='latin1', sep=';', dtype=str)
mapper = df_b3_instruments.groupby(['CrpnNm'])['TckrSymb'].apply(choose_company_tickers).to_dict()

def name_to_ticker(name: str):
    try:
        return mapper[name]
    except KeyError:
        return np.nan

def get_accounts(df):
  # Extract account names
  accounts = df[['CD_CONTA', 'DS_CONTA']].copy()
  accounts['DS_CONTA'] = accounts['DS_CONTA'].str.lower()
  accounts['DS_CONTA'] = accounts['DS_CONTA']\
      .str.normalize('NFKD')\
      .str.encode('ascii', errors='ignore')\
      .str.decode('utf-8')
  accounts = accounts.sort_values('CD_CONTA')
  accounts = accounts.drop_duplicates(keep='first', ignore_index=True)
  accounts_df = pd.DataFrame(accounts)
  accounts_df.set_index('CD_CONTA', inplace=True)
  return accounts_df

def process():
    print('Start process ITRs')
    processed_path = get_processed_path()
    df = load_itr()

    df_clean = clean_itr(df)
    df_clean.to_csv(processed_path)
    print(f'Clean data saved in {processed_path} !')

    print('Downloading account dictionary...')
    df_accounts = get_accounts(df)
    df_accounts.to_csv('./data/processed/accounts.csv')
    print(f'Accouynt data saved in ./data/processed/accounts.csv!')

    process_indicators.process_indicators()
