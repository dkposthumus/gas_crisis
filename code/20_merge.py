import requests
import json
import pandas as pd
from pathlib import Path
# let's create a set of locals referring to our directory and working directory 
home_dir = Path.home()
work_dir = (home_dir / 'gas_crisis')
data = (work_dir / 'data')
raw_data = (data / 'raw')
code = Path.cwd() 

brent_df = pd.read_csv(f'{data}/brent_price.csv')
cpi_df = pd.read_csv(f'{data}/cpi.csv') 
sp500_df = pd.read_csv(f'{data}/sp500.csv')
wti_df = pd.read_csv(f'{data}/wti.csv')
_10yr_df = pd.read_csv(f'{data}/_10_yr.csv')

# now merge all data, focusing on date
master_df = pd.merge(brent_df, cpi_df, on='date', how='outer')
master_df = pd.merge(master_df, sp500_df, on='date', how='outer')
master_df = pd.merge(master_df, wti_df, on='date', how='outer')
master_df = pd.merge(master_df, _10yr_df, on='date', how='outer')

# sort by date for readability
master_df['date'] = pd.to_datetime(master_df['date'])
master_df = master_df.sort_values(by='date')

# now forward fill the cpi data so that it is daily 
ffill_var = ['all-urban cpi', 'real broad dollar']
for var in ffill_var:
    master_df[var] = master_df[var].fillna(
        method='ffill'
    )

# export 
master_df.to_csv(f'{data}/master.csv', index=False)