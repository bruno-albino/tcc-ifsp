#!/usr/bin/bash
cd ./data/downloaded
# metadata
wget --no-clobber http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/META/meta_itr_cia_aberta_txt.zip

# years
for year in $(seq 2020 2020)
do
  wget --no-clobber http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_${year}.zip
done
