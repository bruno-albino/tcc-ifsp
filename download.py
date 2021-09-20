# This files runs following the cron patterns bellow
# CRON_TO_RUN_EVERY_1TH_MONTH = '0 0 1 1 *'
# CRON_TO_RUN_EVERY_4TH_MONTH = '0 0 1 4 *'
# CRON_TO_RUN_EVERY_7TH_MONTH = '0 0 1 7 *'
from main import process
import requests
import zipfile
import io
import os
from datetime import date

directory = './itrs'
basename = 'itr_cia_aberta_'
names = ['DVA', 'DRE', 'DRA', 'DMPL', 'DFC_MI', 'BPP', 'BPA']
secondaries = ['ind', 'con']


def download_itrs(year):
  clear_itrs_folder()
  
  filenames = [basename + year + '.csv']
  for name in names:
    for secondary in secondaries:
      filenames.append(basename + name + '_' + secondary + '_' + year + '.csv')

  url = f'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_{year}.zip'
  res = requests.get(url)
  z = zipfile.ZipFile(io.BytesIO(res.content))

  for filename in filenames:
    info = z.getinfo(name=filename)
    z.extract(info, path=directory)

def clear_itrs_folder():
  files_in_directory = os.listdir(directory)
  filtered_files = [file for file in files_in_directory if file.endswith(".csv")]
  for file in filtered_files:
    path_to_file = os.path.join(directory, file)
    os.remove(path_to_file)


if __name__ == '__main__':
    download_itrs(str(date.today().year))
    process()