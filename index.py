# This files runs following the cron patterns bellow
# CRON_TO_RUN_EVERY_1TH_MONTH = '0 0 1 1 *'
# CRON_TO_RUN_EVERY_4TH_MONTH = '0 0 1 4 *'
# CRON_TO_RUN_EVERY_7TH_MONTH = '0 0 1 7 *'

import requests
import zipfile
import io
import main

year = '2020'
basename = 'itr_cia_aberta_'
names = ['DVA', 'DRE', 'DRA', 'DMPL', 'DFC_MI', 'BPP', 'BPA']
secondaries = ['ind', 'con']

filenames = [basename + year + '.csv']
for name in names:
  for secondary in secondaries:
    filenames.append(basename + name + '_' + secondary + '_' + year + '.csv')


url = f'http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_2020.zip'

res = requests.get(url)
z = zipfile.ZipFile(io.BytesIO(res.content))

for filename in filenames:
  info = z.getinfo(name=filename)
  z.extract(info, path="./itrs")


main.process()
