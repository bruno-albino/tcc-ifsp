import yfinance as yf

def get_quotes_df(tickers):
  serialized_tickers = ' '.join(list(map(lambda ticker: f'{ticker}.sa', tickers)))
  data = yf.download(tickers=serialized_tickers, start="2015-01-01", interval="1d")
  data = data[['Adj Close']]
  data = data.fillna(0)
  return data
