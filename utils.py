def get_itrs_path():
  return './itrs'

def get_itr_names():
  names = ['DVA', 'DRE', 'DRA', 'DMPL', 'DFC_MI', 'BPP', 'BPA']
  # names = ['DRE']
  return names

def get_secondary_documents():
  # secondaries = ['ind', 'con']
  secondaries = ['con']
  return secondaries

def get_quotes_path():
  return './data/processed/quotes.csv'

def get_processed_path():
  return './data/processed/processed.csv'

def get_indicators_path():
  return './data/processed/indicators.csv'
