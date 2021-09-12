import sys
from pathlib import Path
import pandas as pd

def main():
    file = 'data/processed/01_joined-2020-2020.csv'
    df = pd.read_csv(file, sep=',')
    

if __name__ == '__main__':
    main()
