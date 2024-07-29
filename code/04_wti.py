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
wti = fred.get_series('RTWEXBGS')

wti_df = wti.reset_index()
wti_df.columns = ['date', 'real broad dollar']
wti_df['date'] = pd.to_datetime(wti_df['date'])

wti_df.to_csv(f'{data}/wti.csv', index=False)