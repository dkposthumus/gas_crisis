import requests
import json
import pandas as pd
from pathlib import Path
# import matplotlib.pyplot as plt
# let's create a set of locals referring to our directory and working directory 
home_dir = Path.home()
work_dir = (home_dir / 'gas_crisis')
data = (work_dir / 'data')
raw_data = (data / 'raw')
code = Path.cwd() 

bloomberg_df = pd.read_csv(f'{raw_data}/bloomberg_var.csv', header = 3)
bloomberg_df = bloomberg_df.drop([0, 1])
bloomberg_df.rename(
    columns={
        bloomberg_df.columns[0]: 'date',
        'USTWBGD Index': 'nominal broad dollar',
        'USTRBGD Index': 'real broad dollar',
        'CO1 Comdty': 'brent price (nominal)',
        'USGG10YR Index': '10 yr yield',
        'SPX Index': 'sp 500',
        'OPCRTOTL Index': 'opec oil production',
        'OLPRTWLD Index': 'world oil production',
        'EHGDDEV Index': 'opec oil price index',
        'IP Index': 'usa industrial production',
    }, 
    inplace=True
)


bloomberg_df['date'] = pd.to_datetime(bloomberg_df['date'])

bloomberg_df.to_csv(f'{data}/bloomberg_var.csv', index=False)