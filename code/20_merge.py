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

bloomberg_df = pd.read_csv(f'{data}/bloomberg_var.csv')
cpi_df = pd.read_csv(f'{data}/cpi.csv') 
umich_df = pd.read_csv(f'{data}/umich.csv')
opec_kaenzig_df = pd.read_csv(f'{data}/opec_kaenzig.csv')

# now merge all data, focusing on date
master_df = pd.merge(bloomberg_df, cpi_df, on='date', how='outer')
#master_df = pd.merge(master_df, umich_df, on='date', how='outer')
master_df = pd.merge(master_df, opec_kaenzig_df, on='date', how='outer')

# sort by date for readability
master_df['date'] = pd.to_datetime(master_df['date'])
master_df = master_df.sort_values(by='date')

# now forward fill the cpi data so that it is daily 
ffill_var = ['all-urban cpi']
for var in ffill_var:
    master_df[var] = master_df[var].fillna(
        method='ffill'
    )
# now fill all missing observations of the production cut variable with 0, since a production cut did *not* occur there
opec_var = ['meeting', 'no decision', 'production cut', 'production rise', 'production decision']
for var in opec_var:
    master_df[var].fillna(0, inplace=True)

# export 
master_df.to_csv(f'{data}/master.csv', index=False)