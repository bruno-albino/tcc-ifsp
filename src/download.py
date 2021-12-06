# This files runs following the cron patterns bellow
# CRON_TO_RUN_EVERY_1TH_MONTH = '0 0 1 1 *'
# CRON_TO_RUN_EVERY_4TH_MONTH = '0 0 1 4 *'
# CRON_TO_RUN_EVERY_7TH_MONTH = '0 0 1 7 *'
import time
import requests_cache
import zipfile
import io
import os
import pathlib
from utils import get_chromedriver_path, get_download_path, get_itr_names, get_itrs_path
from datetime import date, timedelta
from selenium import webdriver
from pathlib import Path

basename = 'itr_cia_aberta_'
path = get_itrs_path()
download_path = get_download_path()
session = requests_cache.CachedSession('itrs_download_cache')

def download_instrument_consolidated():
  delete_consolidate_files()

  today = date.today()

  # Site da B3 não entrega no final de semana
  if today.weekday() > 4:
    diff = today.weekday() - 4
    today = today - timedelta(days=diff)

  options = webdriver.ChromeOptions()
  prefs = {"download.default_directory" : os.path.join(pathlib.Path(__file__).parent.resolve(), '..', 'data', 'downloaded')}
  options.add_experimental_option("prefs",prefs)
  options.headless = True

  driver = webdriver.Chrome(options=options, executable_path=get_chromedriver_path())
  driver.get(f'https://arquivos.b3.com.br/tabelas/InstrumentsConsolidated/{today}')
  time.sleep(5)
  driver.find_element_by_link_text("Baixar arquivo completo").click()
  time.sleep(5)
  download_wait()
  driver.quit()

def download_wait():
  seconds = 0
  dl_wait = True
  while dl_wait:
      time.sleep(1)
      dl_wait = False
      for fname in os.listdir(os.path.join(pathlib.Path(__file__).parent.resolve(), '..', 'data', 'downloaded')):
          if fname.endswith('.crdownload'):
              dl_wait = True
      seconds += 1
  return seconds

def download_itrs(year):
  clear_itrs_folder()
  
  filenames = [basename + year + '.csv']
  for name in get_itr_names():
    filenames.append(basename + name + '_con_' + year + '.csv')

  url = f'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_{year}.zip'
  res = session.get(url)
  z = zipfile.ZipFile(io.BytesIO(res.content))

  for filename in filenames:
    info = z.getinfo(name=filename)
    z.extract(info, path=path)

def clear_itrs_folder():
  files_in_directory = os.listdir(path)
  filtered_files = [file for file in files_in_directory if file.endswith(".csv")]
  for file in filtered_files:
    path_to_file = os.path.join(path, file)
    os.remove(path_to_file)

def delete_consolidate_files():
  dir = Path(download_path)
  files_to_read = [f for f in list(dir.glob('InstrumentsConsolidatedFile*.csv'))]
  for file in files_to_read:
    os.remove(file)
