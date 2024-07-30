import requests
import json
import pandas as pd
from pathlib import Path
from fredapi import Fred
# let's create a set of locals referring to our directory and working directory 
home_dir = Path.home()
work_dir = (home_dir / 'gas_crisis')
data = (work_dir / 'data')
raw_data = (data / 'raw')
code = Path.cwd() 

fred = Fred(api_key='8905b2f5faefd705486e644f09bb8088')
_10yr = fred.get_series('DGS10')

_10yr_df = _10yr.reset_index()
_10yr_df.columns = ['date', '10 yr yield']
_10yr_df['date'] = pd.to_datetime(_10yr_df['date'])

# filter so that I'm only using observations starting in January 01, 2000
start_date = pd.to_datetime('01/01/2000')
_10yr_df = _10yr_df[_10yr_df['date'] >= start_date]

_10yr_df.to_csv(f'{data}/_10_yr.csv', index=False)