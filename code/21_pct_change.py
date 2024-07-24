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

master_df = pd.read_csv(f'{data}/master.csv')

master_df['date'] = pd.to_datetime(master_df['date'])
master_df.set_index('date', inplace=True)

# i want to calculate a series of daily percent changes
var_daily_chg = ['real broad dollar', '10 yr yield', 's&p 500', 'brent price (nominal)']

for var in var_daily_chg:
    master_df[f'{var} daily pct chg'] = master_df[var].pct_change()
# now i need to find the 4-day cumulative change in the brent crude price
master_df['brent 4-day cumulative pct chg'] = (master_df['brent price (nominal)'].pct_change(4) + 1).pow(4).sub(1)

master_df.to_csv(f'{data}/master.csv', index=False)