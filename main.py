# import sys
# import argparse
from pathlib import Path

# import requests_cache
import numpy as np
import pandas as pd
import yfinance as yf

from tqdm import tqdm

# parser = argparse.ArgumentParser()
# parser.add_argument(
#     '--proxy',
#     default=None,
#     dest='proxy',
#     metavar='IP:PORT',
#     help='Use proxy server to download data with yfinance. '
#     'Must be in the format ip:port [127.0.0.1:1337]'
# )

# cache_group = parser.add_mutually_exclusive_group(required=True)
# cache_group.add_argument(
#     '--cache',
#     help='Use a `requests_cache` session with yfinance',
#     action='store_true'
# )
# cache_group.add_argument(
#     '--no-cache',
#     help='Disable requests cache',
#     action='store_true'
# )

# args = parser.parse_args()

# Warn user about proxy usage
# proxy = args.proxy
# if not args.proxy:
#     print('WARNING: Proxy server not specified')
#     question = 'Do you want to proceed?'
#     choices = ' [y/N]: '
#     default_answer = 'n'
#     reply = str(input(question + choices)).lower().strip() or default_answer
#     if reply[0] == 'y':
#         pass
#     else:
#         parser.print_help()
#         sys.exit(1)

# Create cache session for scraping with yfinance
# if args.cache:
#     session = requests_cache.CachedSession('yfinance.cache')
# elif args.no_cache:
#     session = None


def choose_company_tickers(tickers):
    company_tickers = []

    for t in tickers:
        if len(t) == 5 and (t[-1] == '3' or t[-1] == '4'):
            company_tickers.append(t)

    if len(company_tickers) > 0:
        return company_tickers[0]
    else:
        return np.nan


df_b3_instruments = pd.read_csv(
    'data/downloaded/InstrumentsConsolidatedFile_20210528_1.csv',
    encoding='latin1',
    sep=';',
    dtype=str
)
mapper = df_b3_instruments.groupby(['CrpnNm'])['TckrSymb']\
    .apply(choose_company_tickers)\
    .to_dict()


def load_itr(path,
             itr_names=['BPA', 'BPP', 'DRE', 'DFC_MI', 'DVA']):
    dir = Path(path)
    df = pd.DataFrame()
    print('Loading data...')
    # files_to_read = [f for f in list(dir.glob('itr_cia_aberta_*_con_*.csv'))
    #                  if any(itr in str(f) for itr in itr_names) and
    #                  any(year in str(f) for year in ['2019', '2020'])]
    files_to_read = [f for f in list(dir.glob('itr_cia_aberta_*_con_*.csv'))
                     if any(itr in str(f) for itr in itr_names)]
    for file in tqdm(files_to_read,
                     dynamic_ncols=True):
        df = df.append(pd.read_csv(file, sep=';', encoding='latin1'))

    print(df)
    df = df[df['ORDEM_EXERC'].eq('ÚLTIMO')].reset_index(drop=True)
    return df


def clean_itr(df):
    temp = df.copy()
    # Drop lines referring to penultimate accounting period, otherwise there
    # would be duplicated values when we load more than one consecutive year.
    temp = temp[temp['ORDEM_EXERC'].eq('ÚLTIMO')].reset_index(drop=True)

    # Extract account names
    accounts = temp[['CD_CONTA', 'DS_CONTA']].copy()
    accounts['DS_CONTA'] = accounts['DS_CONTA'].str.lower()
    accounts['DS_CONTA'] = accounts['DS_CONTA']\
        .str.normalize('NFKD')\
        .str.encode('ascii', errors='ignore')\
        .str.decode('utf-8')
    accounts = accounts.sort_values('CD_CONTA')
    accounts = accounts.drop_duplicates(keep='first', ignore_index=True)

    # Remove duplicated rows with different account names
    try:
        temp = temp.sort_values('DT_INI_EXERC')
    except KeyError:
        pass
    temp = temp.groupby(['DT_REFER',
                         'DENOM_CIA',
                        'CD_CONTA']).last().reset_index()

    # Remove unused columns
    temp = temp[['CNPJ_CIA', 'DT_REFER', 'DENOM_CIA', 'CD_CVM',
                 'CD_CONTA', 'VL_CONTA']]

    # (Hopefully) Remove the remaining duplicated rows
    temp = temp.drop_duplicates(keep='last', ignore_index=True)

    return temp, accounts


def extract_features_itr(df):
    agg = df.groupby(['DT_REFER', 'CD_CVM'])[['CNPJ_CIA', 'DENOM_CIA']].last()
    features = df.pivot_table(
        index=['DT_REFER', 'CD_CVM'],
        columns='CD_CONTA',
        values='VL_CONTA'
        # aggfunc='last'
    )

    return pd.concat([agg, features], axis=1).reset_index()\
                                             .rename_axis(None, axis=1)


def name_to_ticker(name: str):
    try:
        return mapper[name]
    except KeyError:
        return np.nan


def add_tickers(df):
    temp = df.copy()
    temp.insert(
        loc=temp.columns.get_loc('DENOM_CIA') + 1,
        column='TICKER',
        value=temp['DENOM_CIA'].apply(name_to_ticker)
    )
    return temp


def get_quotes(df):
    df_quotes = pd.DataFrame()
    for ticker, df_cia in df.groupby('TICKER'):
        start_date = df_cia['DT_REFER'].min()[0:8] + '01'
        end_date = df_cia['DT_REFER'].max()[0:8] + '01'
        ticker_yf = ticker + '.SA'
        data = yf.download(tickers=ticker_yf,
                           start=start_date,
                           end=end_date,
                           interval='1mo').reset_index()
        data['TICKER'] = ticker
        df_quotes = df_quotes.append(data, ignore_index=True)

    return df_quotes.dropna().groupby([pd.Grouper(key='Date', freq='M'),
                                       'TICKER']).first().reset_index()


def process():
    path = 'itrs'
    processed_path = 'data/processed'
    df = load_itr(path)
    df['TICKER'] = df['DENOM_CIA'].apply(name_to_ticker)
    
    # grab years range
    years = sorted(df['DT_REFER'].unique().tolist())
    start_year = years[0].split('-')[0]
    end_year = years[-1].split('-')[0]
    processed_range_file_end = f'-{start_year}-{end_year}.csv'
    
    # save joined data
    print('Saving joined data...')
    path = f'{processed_path}/01_joined{processed_range_file_end}'
    df.to_csv(path)
    print(f'Joined ITR data saved in `{path}` !')

    # save accounts dictionary
    print('Saving accounts dictionary...')
    df_clean, df_accounts = clean_itr(df)
    path = f'{processed_path}/accounts{processed_range_file_end}'
    df_accounts.to_csv(path)
    print(f'Accounts dictionary data saved in {path} !')

    print('Extracting features...')
    df_features = extract_features_itr(df_clean)

    # save tickers
    print('Getting tickers...')
    df_tickers = add_tickers(df_features)
    print('Saving tickers data...')
    path = f'{processed_path}/04_tickers{processed_range_file_end}'
    df_tickers.to_csv(path)
    print(f'Ticker data saved in `{path}` !')

    # save quotes
    print('Downloading quotes (adjusted close price) data...')
    df_quotes = get_quotes(df_tickers)
    print('Saving quotes data...')
    path = f'{processed_path}/05-quotes{processed_range_file_end}'
    df_quotes.to_csv(path)
    print(f'Quote data saved in `{path}` !')

if __name__ == '__main__':
    process()
