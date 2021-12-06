
from pathlib import Path
from download import download_instrument_consolidated
from utils import get_download_path


download_instrument_consolidated()
dir = Path(get_download_path())
file = [f for f in list(dir.glob('InstrumentsConsolidatedFile*.csv'))][0]
df_b3_instruments = pd.read_csv(file, encoding='latin1', sep=';', dtype=str)

def choose_company_tickers(tickers):
    company_tickers = []

    for t in tickers:
        if len(t) == 5 and (t[-1] == '3' or t[-1] == '4'):
            company_tickers.append(t)

    if len(company_tickers) > 0:
        return company_tickers[0]
    else:
        return np.nan

def init():
  mapper = df_b3_instruments.groupby(['CrpnNm'])['TckrSymb'].apply(choose_company_tickers).to_dict()
  print(mapper)

if __name__ == '__main__':
    init()
