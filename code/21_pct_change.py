import requests
import json
import pandas as pd
from pathlib import Path
import subprocess
# import matplotlib.pyplot as plt
# let's create a set of locals referring to our directory and working directory 
home_dir = Path.home()
work_dir = (home_dir / 'gas_crisis')
data = (work_dir / 'data')
raw_data = (data / 'raw')
code = Path.cwd() 

python='/Library/Frameworks/Python.framework/Versions/3.12/bin/python3'
# run merge python file
subprocess.run([python, f'{code}/20_merge.py'], check=True)

master_df = pd.read_csv(f'{data}/master.csv')

master_df['date'] = pd.to_datetime(master_df['date'])
master_df.set_index('date', inplace=True)

# bloomberg variables are only available for trading days; 
# thus, i'll pick nominal broad dollar and drop if it's NaN
master_df = master_df.dropna(subset=['nominal broad dollar'])

# i want to calculate a series of daily percent and level changes
var_daily_chg = ['nominal broad dollar', 'real broad dollar', '10 yr yield', 'sp 500', 'brent price (nominal)']

for var in var_daily_chg:
    master_df[f'{var} daily pct chg'] = master_df[var].pct_change().abs()*100
    master_df[f'{var} daily chg'] = master_df[var].diff().abs()
# now i need to find the 4-day cumulative change in the brent crude price
master_df['brent 4-day cumulative pct chg'] = (master_df['brent price (nominal)'].pct_change(4) + 1).pow(4).sub(1)

master_df.to_csv(f'{data}/master.csv', index=True)