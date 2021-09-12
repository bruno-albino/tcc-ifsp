#!/usr/bin/bash
# create raw folder
mkdir ./data/raw
mkdir ./data/raw/itr-2019-2020

# navigate to zips folder
cd ./data/downloaded

# Extract it by passing the raw folder path (default ../raw/itr)
for file in *.zip
do
  unzip -n $file -d $(basename -s .zip $file)
  unzip -n $file -d  ../raw/itr-2020
  rm $file
done


