from pathlib import Path
import numpy as np
import pandas as pd
import yfinance as yf
import process_indicators 
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


df_b3_instruments = pd.read_csv(
    'data/downloaded/InstrumentsConsolidatedFile_20210528_1.csv',
    encoding='latin1',
    sep=';',
    dtype=str
)
mapper = df_b3_instruments.groupby(['CrpnNm'])['TckrSymb']\
    .apply(choose_company_tickers)\
    .to_dict()

def load_itr(path):
    itr_names = ['BPA', 'BPP', 'DRE', 'DFC_MI', 'DVA']
    dir = Path(path)
    df = pd.DataFrame()
    print('Loading data...')

    files_to_read = [f for f in list(dir.glob('itr_cia_aberta_*_con_*.csv'))
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
    temp = temp[['CNPJ_CIA', 'DT_REFER', 'DENOM_CIA', 'CD_CVM',
                 'CD_CONTA', 'VL_CONTA']]

    # (Hopefully) Remove the remaining duplicated rows
    temp = temp.drop_duplicates(keep='last', ignore_index=True)

    return temp


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

def process():
    path = 'itrs'
    processed_path = 'data/processed'
    df = load_itr(path)
    
    # # grab years range
    # years = sorted(df['DT_REFER'].unique().tolist())
    # start_year = years[0].split('-')[0]
    # end_year = years[-1].split('-')[0]
    # processed_range_file_end = f'-{start_year}-{end_year}.csv'
    # processed_range_file_end = f'.csv'
    
    # save joined data
    # print('Saving joined data...')
    # path = f'{processed_path}/01-joined{processed_range_file_end}'
    # df.to_csv(path)
    # print(f'Joined ITR data saved in `{path}` !')

    # save accounts dictionary
    print('Cleaning data...')
    df_clean = clean_itr(df)
    df_clean.set_index('CD_CONTA', inplace=True)
    path = f'{processed_path}/processed.csv'
    df_clean.to_csv(path)
    print(f'Clean data saved in {path} !')
    process_indicators.process_indicators(df_clean)
    

    # print('Extracting features...')
    # df_features = extract_features_itr(df_clean)
    # path = f'{processed_path}/03-feature{processed_range_file_end}'
    # df_clean.to_csv(path)
    # print(f'Feature data saved in {path} !')

    # # save tickers
    # print('Getting tickers...')
    # df_tickers = add_tickers(df_features)
    # print('Saving tickers data...')
    # path = f'{processed_path}/04-tickers{processed_range_file_end}'
    # df_tickers.to_csv(path)
    # print(f'Ticker data saved in `{path}` !')

if __name__ == '__main__':
    process()
